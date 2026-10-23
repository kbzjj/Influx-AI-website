#!/usr/bin/env python3
"""Localize the approved Veo pages and their public Framer ESM dependency graph.

The approved page list comes from scope.json. No other websites are crawled.
Run with --page-cache to reuse captured original HTML during this migration.
"""
import argparse
import concurrent.futures
import hashlib
import html
import json
from pathlib import Path
import posixpath
import re
import time
from urllib.parse import urljoin, urlsplit, urldefrag
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://veo.framer.ai'
MEDIA = re.compile(r'https://(?:framerusercontent\.com|fonts\.gstatic\.com)/(?:(?!&quot;|&#34;|&#x22;)[^\s"\'`<>\\(),])+')
IMPORT = re.compile(r'(["\'`])((?:\./|\.\./)[^"\'`\s]+\.mjs)\1')
CMS = re.compile(r'new URL\((["\'`])([^"\'`]+\.framercms)\1,\s*(["\'`])(https://framerusercontent\.com/[^"\'`]+)\3\)\.href\.replace\((["\'`])/modules/\5,\s*(["\'`])/cms/\6\)')
EXTENSIONS = {'.mjs', '.js', '.css', '.json', '.framercms', '.woff', '.woff2', '.ttf', '.otf', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif', '.mp4', '.webm'}


def resources(source, base):
    found = set()
    for value in MEDIA.findall(html.unescape(source)):
        url = urldefrag(value)[0]
        if Path(urlsplit(url).path).suffix.lower() in EXTENSIONS:
            found.add(url)
    if base.endswith('.mjs'):
        found.update(urljoin(base, m.group(2)) for m in IMPORT.finditer(source))
    found.update(urljoin(m.group(4), m.group(2)).replace('/modules/', '/cms/') for m in CMS.finditer(source))
    return found


def path_for(url):
    parts = urlsplit(url)
    name = parts.path.rsplit('/', 1)[-1]
    digest = hashlib.sha256(url.encode()).hexdigest()[:16]
    if parts.path.endswith('.mjs'):
        parent = hashlib.sha256((parts.netloc + posixpath.dirname(parts.path)).encode()).hexdigest()[:10]
        return 'runtime/' + parent + '/' + name
    return 'assets/' + digest + '-' + name


def get(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60) as response:
                return response.read(), response.headers.get_content_type()
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--page-cache')
    args = parser.parse_args()
    scope = json.loads((ROOT / 'scope.json').read_text())
    pages = {}
    cache = json.loads(Path(args.page_cache).read_text()) if args.page_cache else {}
    for url in scope['included_pages']:
        source = Path(cache[url]).read_text() if url in cache else get(url)[0].decode()
        route = urlsplit(url).path
        path = 'index.html' if route == '/' else route.strip('/') + '/index.html'
        pages[url] = {'path': path, 'source': source}
        original = ROOT / '_source/pages' / path
        original.parent.mkdir(parents=True, exist_ok=True)
        original.with_suffix('.html.txt').write_text(source)

    previous = {}
    previous_path = ROOT / 'downloaded-assets.json'
    if previous_path.exists():
        for item in json.loads(previous_path.read_text()):
            if item.get('downloaded') and (ROOT / item['file']).exists():
                previous[item['url']] = item['file']
    cached_raw = ROOT / '_source/resources'
    cached_raw.mkdir(parents=True, exist_ok=True)
    manifest_path = ROOT / 'asset-manifest.json'
    prior_manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for item in prior_manifest.get('assets', []):
        if (ROOT / item.get('raw_path', '_absent')).is_file():
            previous[item['url']] = item['raw_path']
        elif (ROOT / item['path']).is_file() and Path(urlsplit(item['url']).path).suffix not in ('.mjs', '.js', '.css', '.json'):
            previous[item['url']] = item['path']

    assets, raw, failures = {}, {}, {}
    pending = set().union(*(resources(page['source'], url) for url, page in pages.items()))
    attempted = set()

    def download(url):
        if url in previous:
            data = (ROOT / previous[url]).read_bytes()
            ctype = 'text/javascript' if urlsplit(url).path.endswith('.mjs') else 'application/octet-stream'
        else:
            raw_file = cached_raw / hashlib.sha256(url.encode()).hexdigest()
            if raw_file.exists():
                data = raw_file.read_bytes()
                ctype = 'text/javascript' if urlsplit(url).path.endswith('.mjs') else 'application/octet-stream'
            else:
                data, ctype = get(url)
                raw_file.write_bytes(data)
        return data, ctype

    while pending:
        batch = sorted(pending - attempted)
        pending = set()
        if not batch:
            break
        attempted.update(batch)
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
            futures = {pool.submit(download, url): url for url in batch}
            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                try:
                    data, ctype = future.result()
                    path = path_for(url)
                    ext = Path(urlsplit(url).path).suffix.lower()
                    raw[url] = data
                    record = {'url': url, 'path': path, 'bytes': len(data), 'content_type': ctype}
                    assets[url] = record
                    if ext in ('.mjs', '.js', '.css', '.json'):
                        raw_path = '_source/resources/' + hashlib.sha256(url.encode()).hexdigest()
                        (ROOT / raw_path).write_bytes(data)
                        record['raw_path'] = raw_path
                        pending.update(resources(data.decode('utf-8'), url) - attempted)
                    if len(assets) % 100 == 0:
                        print('Resources:', len(assets), flush=True)
                except Exception as error:
                    failures[url] = str(error)
        print('Dependency round:', len(assets), 'saved;', len(pending), 'new references;', len(failures), 'failures', flush=True)

    def rewrite_resources(source, current):
        def replace(match):
            original = match.group()
            decoded = html.unescape(original)
            base, fragment = urldefrag(decoded)
            if base not in assets:
                return original
            return '/' + assets[base]['path'] + ('#' + fragment if fragment else '')
        return MEDIA.sub(replace, source)

    for url, item in assets.items():
        data = raw[url]
        ext = Path(urlsplit(url).path).suffix.lower()
        if ext in ('.mjs', '.js', '.css', '.json'):
            source = data.decode('utf-8')
            def replace_cms(match):
                target = urljoin(match.group(4), match.group(2)).replace('/modules/', '/cms/')
                if target in assets:
                    return 'new URL(' + json.dumps('/' + assets[target]['path']) + ',location.origin).href'
                return match.group()
            source = CMS.sub(replace_cms, source)
            source = rewrite_resources(source, item['path'])
            if ext == '.mjs':
                def replace_import(match):
                    target = assets.get(urljoin(url, match.group(2)))
                    if not target:
                        return match.group()
                    relative = posixpath.relpath(target['path'], posixpath.dirname(item['path']))
                    if not relative.startswith('.'):
                        relative = './' + relative
                    return match.group(1) + relative + match.group(1)
                source = IMPORT.sub(replace_import, source)
            data = source.encode()
        target = ROOT / item['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        item['sha256'] = hashlib.sha256(data).hexdigest()
        item['saved_bytes'] = len(data)

    for url, item in pages.items():
        source = rewrite_resources(item['source'], item['path'])
        # Drop only the analytics script; retain every visual/runtime component.
        source = re.sub(r'<script\b[^>]*src="https://events\.framer\.com/[^>]*></script>', '', source)
        def rewrite_link(match):
            href = html.unescape(match.group(2))
            if not href or href.startswith('#'):
                return match.group()
            absolute = urljoin(url, href)
            parsed = urlsplit(absolute)
            if parsed.netloc == 'veo.framer.ai':
                target = ORIGIN + (parsed.path.rstrip('/') or '/')
                if target in pages:
                    href = parsed.path.rstrip('/') or '/'
                    if parsed.fragment:
                        href += '#' + parsed.fragment
                    return 'href=' + match.group(1) + href + match.group(1)
            return match.group()
        source = re.sub(r'href=(["\'])(.*?)\1', rewrite_link, source)
        source = source.replace('</head>', '<script src="/local-preview.js"></script></head>')
        target = ROOT / item['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source)

    manifest = {'source': ORIGIN, 'captured_on': '2026-10-23',
                'pages': [{'url': url, 'path': item['path']} for url, item in pages.items()],
                'assets': list(assets.values()), 'failures': failures,
                'runtime': 'Original Framer ESM graph with local static resource URLs and original routing'}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    retained_raw = {item.get('raw_path') for item in assets.values() if item.get('raw_path')}
    for cache_file in cached_raw.iterdir():
        if str(cache_file.relative_to(ROOT)) not in retained_raw:
            cache_file.unlink()
    print(json.dumps({'pages': len(pages), 'assets': len(assets), 'media_mb': round(sum(a['saved_bytes'] for a in assets.values()) / 1024 / 1024, 1), 'failures': failures}, ensure_ascii=False, indent=2), flush=True)
    return 2 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
