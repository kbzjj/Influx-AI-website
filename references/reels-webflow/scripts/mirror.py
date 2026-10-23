#!/usr/bin/env python3
"""Save the public Reels demo, its linked pages, and front-end dependencies.

Only GET requests are made. Existing Influx pages are never changed.
Run from any directory: python3 references/reels-webflow/scripts/mirror.py
"""
import concurrent.futures
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import posixpath
import re
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://reels-wbs.webflow.io'
HOSTS = {'cdn.prod.website-files.com', 'cdn.jsdelivr.net', 'unpkg.com',
         'd3e54v103j8qbb.cloudfront.net', 'ajax.googleapis.com', 'fonts.gstatic.com'}
URL_RE = re.compile(r'https?://[^\s<>"\'()\\,]+')
CSS_URL_RE = re.compile(r'url\(\s*["\']?([^\s"\')]+)["\']?\s*\)')
pages, assets, failures = {}, {}, {}
CACHE = json.loads((ROOT / 'asset-manifest.json').read_text()).get('assets', {}) if (ROOT / 'asset-manifest.json').exists() else {}


def fetch(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=90) as response:
                return response.read(), response.headers.get('Content-Type', '')
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def page_path(route):
    return Path(route.lstrip('/')) / 'index.html' if route != '/' else Path('index.html')


def relative(target, current):
    return posixpath.relpath(str(target), str(current.parent))


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        href = dict(attrs).get('href', '')
        parsed = urllib.parse.urlsplit(urllib.parse.urljoin(ORIGIN, href))
        if parsed.netloc == urllib.parse.urlsplit(ORIGIN).netloc:
            if not Path(parsed.path).suffix:
                self.links.add(parsed.path.rstrip('/') or '/')


def asset_path(url):
    name = Path(urllib.parse.unquote(urllib.parse.urlsplit(url).path)).name
    name = re.sub(r'[^a-zA-Z0-9._-]+', '-', name)[-140:] or 'resource'
    return Path('assets') / (hashlib.sha256(url.encode()).hexdigest()[:10] + '-' + name)


def resource_urls(source):
    return {html.unescape(u) for u in URL_RE.findall(html.unescape(source))
            if urllib.parse.urlsplit(html.unescape(u)).netloc in HOSTS
            and Path(urllib.parse.urlsplit(html.unescape(u)).path).suffix}


def save_asset(url):
    cached = CACHE.get(url)
    if cached and (ROOT / cached['path']).exists() and not cached['path'].endswith('.css'):
        return url, cached
    data, content_type = fetch(url)
    path = asset_path(url)
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return url, {'path': str(path), 'bytes': len(data), 'type': content_type}


def main():
    pending = {'/'}
    while pending:
        batch = sorted(pending - pages.keys() - failures.keys())
        if not batch:
            break
        pending = set()
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            futures = {pool.submit(fetch, ORIGIN + route): route for route in batch}
            for future in concurrent.futures.as_completed(futures):
                route = futures[future]
                try:
                    data, _ = future.result()
                    source = data.decode('utf-8')
                    pages[route] = source
                    links = Links()
                    links.feed(source)
                    pending.update(links.links)
                    print('Page:', route, flush=True)
                except Exception as error:
                    failures[route] = str(error)
        if len(pages) > 60:
            raise RuntimeError('Unexpected crawl size; inspect links before continuing.')

    required = set().union(*(resource_urls(s) for s in pages.values()))
    # WebFont normally fetches this at runtime. Keep Boldonse local as well.
    font_css, _ = fetch('https://fonts.googleapis.com/css2?family=Boldonse&display=swap')
    font_css = font_css.decode('utf-8')
    required.update(resource_urls(font_css))
    while required:
        batch = sorted(required - assets.keys() - failures.keys())
        if not batch:
            break
        required = set()
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
            futures = {pool.submit(save_asset, url): url for url in batch}
            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                try:
                    _, metadata = future.result()
                    assets[url] = metadata
                    if 'text/css' in metadata['type'] or metadata['path'].endswith('.css'):
                        source = (ROOT / metadata['path']).read_text()
                        for dep in CSS_URL_RE.findall(source):
                            if not dep.startswith(('data:', '#')):
                                required.add(urllib.parse.urljoin(url, dep))
                except Exception as error:
                    failures[url] = str(error)
        print('Assets saved:', len(assets), flush=True)

    for url, metadata in assets.items():
        if 'text/css' not in metadata['type'] and not metadata['path'].endswith('.css'):
            continue
        path = Path(metadata['path'])
        source = (ROOT / path).read_text()
        def rewrite_css(match):
            dep = urllib.parse.urljoin(url, match.group(1))
            return 'url("' + relative(Path(assets[dep]['path']), path) + '")' if dep in assets else match.group(0)
        (ROOT / path).write_text(CSS_URL_RE.sub(rewrite_css, source))

    font_css = URL_RE.sub(lambda m: relative(Path(assets[m.group()]['path']), Path('assets/fonts.css'))
                         if m.group() in assets else m.group(), font_css)
    (ROOT / 'assets/fonts.css').write_text(font_css)

    for route, source in pages.items():
        path = page_path(route)
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        # Rewriting only URLs preserves whitespace and all Webflow animation IDs.
        for url in sorted(assets, key=len, reverse=True):
            source = source.replace(url, relative(Path(assets[url]['path']), path))
            source = source.replace(html.escape(url, quote=True), relative(Path(assets[url]['path']), path))
        source = re.sub(r'\s+(?:integrity|crossorigin)="[^"]*"', '', source)
        source = re.sub(r'<link\b[^>]*rel="preconnect"[^>]*>', '', source)
        source = re.sub(r'WebFont\.load\(.*?\);', "document.documentElement.classList.add('wf-active');", source)
        source = source.replace('</head>', '<link rel="stylesheet" href="' + relative(Path('assets/fonts.css'), path) + '"></head>')
        def rewrite_link(match):
            href = html.unescape(match.group(1))
            parsed = urllib.parse.urlsplit(urllib.parse.urljoin(ORIGIN + route, href))
            normalized = parsed.path.rstrip('/') or '/'
            if parsed.netloc == urllib.parse.urlsplit(ORIGIN).netloc and normalized in pages:
                result = relative(page_path(normalized), path)
                if parsed.query:
                    result += '?' + parsed.query
                if parsed.fragment:
                    result += '#' + parsed.fragment
                return 'href="' + html.escape(result, quote=True) + '"'
            return match.group(0)
        source = re.sub(r'href="([^"]*)"', rewrite_link, source)
        source = source.replace('</body>', '<script src="' + relative(Path('local-study.js'), path) + '"></script></body>')
        target.write_text(source)

    manifest = {
        'source': ORIGIN, 'captured_on': '2026-10-23',
        'pages': {route: str(page_path(route)) for route in sorted(pages)},
        'assets': dict(sorted(assets.items())), 'failures': failures,
    }
    (ROOT / 'asset-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'pages': len(pages), 'assets': len(assets), 'failures': failures}, indent=2), flush=True)


if __name__ == '__main__':
    main()
