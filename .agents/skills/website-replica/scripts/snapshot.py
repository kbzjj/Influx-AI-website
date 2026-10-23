#!/usr/bin/env python3
"""Localize explicitly selected public HTML pages and their static dependencies.

Standard library only. No recursive page crawl, JavaScript execution, or uploads.
This is a static migration helper, not a universal SPA/runtime exporter.
"""
import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
import mimetypes
from pathlib import Path
import posixpath
import re
import shutil
import sys
from datetime import datetime, timezone
from urllib.parse import quote, urldefrag, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen


ATTR = re.compile(r'''(\s+)([\w:-]+)(\s*=\s*)(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))''')
CSS = re.compile(r'''url\(\s*(?:(["'])(.*?)\1|([^\s)"']+))\s*\)|@import\s+(["'])(.*?)\4''', re.I | re.S)
SINGLE = {'src', 'poster', 'data-src', 'data-poster-url'}
SET = {'srcset', 'imagesrcset', 'data-srcset'}


def web_url(value, base):
    value = value.strip()
    if not value or value.startswith('#'):
        return None
    url = urldefrag(urljoin(base, value))[0]
    parts = urlsplit(url)
    if parts.scheme not in ('http', 'https') or not parts.netloc:
        return None
    if parts.username or parts.password:
        raise ValueError('Only public URLs without embedded credentials are supported.')
    host = parts.hostname.encode('idna').decode('ascii')
    if ':' in host:
        host = '[' + host + ']'
    if parts.port:
        host += ':' + str(parts.port)
    return urlunsplit((parts.scheme, host,
                       quote(parts.path or '/', safe="/:@!$&'()*+,;=-._~%"),
                       quote(parts.query, safe="=&?/:@!$'()*+,;[]%-._~"), ''))


def srcset_parts(value):
    """Parse ordinary srcset candidates, retaining commas inside data URLs."""
    result, i = [], 0
    while i < len(value):
        while i < len(value) and (value[i].isspace() or value[i] == ','):
            i += 1
        start = i
        while i < len(value) and not value[i].isspace():
            i += 1
        url = value[start:i]
        if not url:
            break
        if url.endswith(','):
            result.append((url.rstrip(','), ''))
            continue
        start = i
        while i < len(value) and value[i] != ',':
            i += 1
        result.append((url, value[start:i].strip()))
        i += 1
    return result


def css_refs(source):
    return [m.group(2) if m.group(1) else m.group(3) if m.group(3) is not None else m.group(5)
            for m in CSS.finditer(source)]


def rewrite_css(source, convert):
    def replace(match):
        old = match.group(2) if match.group(1) else match.group(3) if match.group(3) is not None else match.group(5)
        new = convert(old)
        if old == new:
            return match.group()
        escaped = new.replace('\\', '\\\\').replace('"', '\\"')
        return ('@import "' if match.group(4) else 'url("') + escaped + ('"' if match.group(4) else '")')
    return CSS.sub(replace, source)


def resource_link(node):
    if node['tag'] != 'link':
        return False
    rel = (node['attrs'].get('rel') or '').lower().split()
    if (node['attrs'].get('as') or '').lower() == 'document':
        return False
    return bool(set(rel) & {'stylesheet', 'icon', 'apple-touch-icon', 'preload', 'modulepreload'})


def node_resources(node):
    d = node['attrs']
    for key in SINGLE:
        if d.get(key) and node['tag'] != 'iframe':
            yield d[key]
    if (resource_link(node) or node['tag'] in ('use', 'image', 'feimage')) and d.get('href'):
        yield d['href']
    if node['tag'] in ('use', 'image', 'feimage') and d.get('xlink:href'):
        yield d['xlink:href']
    for key in SET:
        for value, _ in srcset_parts(d.get(key, '')):
            yield value
    for value in d.get('data-video-urls', '').split(','):
        if value:
            yield value
    yield from css_refs(d.get('style', ''))


class Document(HTMLParser):
    """Locate only tags and style text; preserve all other HTML bytes verbatim."""
    def __init__(self, source, url):
        super().__init__(convert_charrefs=False)
        self.source, self.base = source, url
        self.nodes, self.styles = [], []
        self.in_style = False
        self.lines = [0]
        self.lines.extend(m.end() for m in re.finditer('\n', source))
        self.feed(source)
        for node in self.nodes:
            if node['tag'] == 'base' and node['attrs'].get('href'):
                self.base = urljoin(url, node['attrs']['href'])
                break

    def position(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        raw = self.get_starttag_text()
        start = self.position()
        self.nodes.append({'tag': tag, 'attrs': dict(attrs), 'raw': raw, 'start': start, 'end': start + len(raw)})
        if tag == 'style':
            self.in_style = True

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag == 'style':
            self.in_style = False

    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False

    def handle_data(self, data):
        if self.in_style:
            self.styles.append((self.position(), self.position() + len(data), data))

    def resources(self):
        for node in self.nodes:
            for value in node_resources(node):
                url = web_url(value, self.base)
                if url:
                    yield url
        for _, _, data in self.styles:
            for value in css_refs(data):
                url = web_url(value, self.base)
                if url:
                    yield url


def local_asset_path(url, content_type):
    # Decode neither encoded slashes nor traversal components into directories.
    name = urlsplit(url).path.rsplit('/', 1)[-1]
    name = re.sub(r'[^a-zA-Z0-9._-]+', '-', name)[-110:] or 'resource'
    if not Path(name).suffix:
        name += '.css' if content_type == 'text/css' else mimetypes.guess_extension(content_type) or '.bin'
    return 'assets/' + hashlib.sha256(url.encode()).hexdigest()[:16] + '-' + name


def relpath(target, current):
    return posixpath.relpath(target, posixpath.dirname(current) or '.')


class Snapshot:
    def __init__(self, args):
        self.args, self.root = args, Path(args.output).resolve()
        self.pages, self.assets, self.failures, self.runtime = {}, {}, [], []
        self.total = 0

    def fetch(self, url):
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (LocalFrontendSnapshot)'})
        with urlopen(request, timeout=30) as response:
            final = response.geturl()
            content_type = response.headers.get_content_type()
            encoding = response.headers.get_content_charset() or 'utf-8'
            data = bytearray()
            while True:
                chunk = response.read(65536)
                if not chunk:
                    break
                self.total += len(chunk)
                data.extend(chunk)
                if len(data) > self.args.max_file_mb * 1024 * 1024:
                    raise ValueError('max-file-mb exceeded; confirm media requirements before increasing it')
                if self.total > self.args.max_total_mb * 1024 * 1024:
                    raise ValueError('max-total-mb exceeded; confirm requirements before increasing it')
            return bytes(data), content_type, encoding, final

    def write(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data if isinstance(data, bytes) else data.encode('utf-8'))

    def convert(self, value, base, current, navigation=False):
        url = web_url(value, base)
        if not url:
            return value
        record = self.pages.get(url) if navigation else None
        record = record or self.assets.get(url)
        fragment = urlsplit(value).fragment
        suffix = '#' + fragment if fragment else ''
        # Uncaptured relative URLs must remain remote, not become broken local links.
        return (relpath(record['path'], current) if record else url) + suffix

    def rewrite_document(self, doc, current):
        replacements = []
        for node in doc.nodes:
            d, tag = node['attrs'], node['tag']
            modified_integrity = False
            if resource_link(node):
                asset = self.assets.get(web_url(d.get('href', ''), doc.base))
                modified_integrity = bool(asset and asset.get('modified'))

            def replace_attr(match):
                key = match.group(2).lower()
                value = html.unescape(next(v for v in match.groups()[3:] if v is not None))
                new = value
                if tag == 'base' and key == 'href':
                    return ''
                if key == 'integrity' and modified_integrity:
                    return ''
                if key in SINGLE or key in ('href', 'xlink:href'):
                    if key in SINGLE or tag in ('a', 'area', 'use', 'image', 'feimage') or resource_link(node):
                        new = self.convert(value, doc.base, current, navigation=tag in ('a', 'area', 'iframe'))
                elif key in SET:
                    new = ', '.join(self.convert(u, doc.base, current) + (' ' + desc if desc else '')
                                    for u, desc in srcset_parts(value))
                elif key == 'data-video-urls':
                    new = ','.join(self.convert(u.strip(), doc.base, current) for u in value.split(','))
                elif key == 'style':
                    new = rewrite_css(value, lambda v: self.convert(v, doc.base, current))
                if new == value:
                    return match.group()
                return match.group(1) + match.group(2) + match.group(3) + '"' + html.escape(new, quote=True) + '"'

            if tag == 'meta' and d.get('charset'):
                # Saved text is UTF-8 regardless of source encoding.
                raw = re.sub(r'(?i)(charset\s*=\s*)(["\']?)[^\s"\'>/]+\2', r'\1"utf-8"', node['raw'])
            elif tag == 'link' and (d.get('rel', '').lower() in ('preconnect', 'dns-prefetch')
                                    or d.get('as', '').lower() == 'document'):
                raw = ''
            else:
                raw = ATTR.sub(replace_attr, node['raw'])
            replacements.append((node['start'], node['end'], raw))
        for start, end, data in doc.styles:
            replacements.append((start, end, rewrite_css(data, lambda v: self.convert(v, doc.base, current))))
        source = doc.source
        for start, end, replacement in sorted(replacements, reverse=True):
            source = source[:start] + replacement + source[end:]
        adapter = '<script src="' + relpath('local-preview.js', current) + '"></script>'
        source, count = re.subn(r'(?i)<head\b[^>]*>', lambda m: m.group() + adapter, source, count=1)
        return source if count else adapter + source

    def run(self):
        if self.root.exists() and (not self.root.is_dir() or any(self.root.iterdir())):
            raise ValueError('Output must be a new or empty directory; existing work will not be overwritten.')
        self.root.mkdir(parents=True, exist_ok=True)
        urls = list(dict.fromkeys(web_url(u, '') for u in self.args.url))
        if not all(urls):
            raise ValueError('Every --url must be an absolute HTTP(S) URL.')
        documents = []
        for index, url in enumerate(urls):
            try:
                data, ctype, encoding, final = self.fetch(url)
                if ctype not in ('text/html', 'application/xhtml+xml'):
                    raise ValueError('Selected page is not HTML: ' + ctype)
                source = data.decode(encoding)
                digest = hashlib.sha256(url.encode()).hexdigest()[:16]
                path = 'index.html' if index == 0 else 'pages/' + digest + '/index.html'
                record = {'url': url, 'final_url': final, 'path': path, 'source_path': '_source/' + digest + '.html.txt'}
                self.pages[url] = record
                self.pages.setdefault(final, record)
                self.write(record['source_path'], data)
                doc = Document(source, final)
                documents.append((record, doc))
                print('Selected page saved:', url, flush=True)
                for node in doc.nodes:
                    d = node['attrs']
                    if node['tag'] == 'script' and d.get('src'):
                        self.runtime.append({'page': url, 'kind': 'script-dependency-review', 'url': urljoin(doc.base, d['src'])})
                    if node['tag'] == 'iframe' and d.get('src'):
                        self.runtime.append({'page': url, 'kind': 'remote-embed', 'url': urljoin(doc.base, d['src'])})
                    if node['tag'] == 'meta' and d.get('http-equiv', '').lower() == 'content-security-policy':
                        self.runtime.append({'page': url, 'kind': 'csp-review'})
            except Exception as error:
                self.failures.append({'url': url, 'kind': 'page', 'error': str(error)})

        extra_urls = [web_url(u, '') for u in self.args.asset]
        if not all(extra_urls):
            raise ValueError('Every --asset must be an absolute HTTP(S) URL.')
        pending = set(extra_urls)
        for _, doc in documents:
            pending.update(doc.resources())
        seen, css_sources = set(), {}
        while pending:
            url = min(pending)
            pending.remove(url)
            url = web_url(url, '')
            if not url or url in seen:
                continue
            if len(seen) >= self.args.max_assets or self.total >= self.args.max_total_mb * 1024 * 1024:
                self.failures.append({'kind': 'limit', 'error': 'Resource count or total-byte limit reached; incomplete output', 'pending_count': len(pending) + 1})
                break
            seen.add(url)
            try:
                data, ctype, encoding, final = self.fetch(url)
                path = local_asset_path(url, ctype)
                record = {'url': url, 'final_url': final, 'path': path, 'content_type': ctype, 'source_bytes': len(data), 'source_sha256': hashlib.sha256(data).hexdigest(), 'modified': False}
                self.assets[url] = record
                self.write(path, data)
                if ctype == 'text/css':
                    source = data.decode(encoding)
                    css_sources[url] = source
                    self.write('_source/' + Path(path).name + '.txt', data)
                    pending.update(u for v in css_refs(source) if (u := web_url(v, final)))
            except Exception as error:
                self.failures.append({'url': url, 'kind': 'asset', 'error': str(error)})
                self.assets.pop(url, None)

        for url, source in css_sources.items():
            record = self.assets[url]
            result = rewrite_css(source, lambda v: self.convert(v, record['final_url'], record['path']))
            result = re.sub(r'(?i)^@charset\s+["\'][^"\']+["\']', '@charset "UTF-8"', result)
            record['modified'] = hashlib.sha256(result.encode('utf-8')).hexdigest() != record['source_sha256']
            self.write(record['path'], result)
        for record, doc in documents:
            self.write(record['path'], self.rewrite_document(doc, record['path']))
        shutil.copyfile(Path(__file__).resolve().parents[1] / 'assets/local-preview.js', self.root / 'local-preview.js')
        for record in self.assets.values():
            saved = (self.root / record['path']).read_bytes()
            record['saved_bytes'] = len(saved)
            record['sha256'] = hashlib.sha256(saved).hexdigest()
        manifest = {'captured_at': datetime.now(timezone.utc).isoformat(), 'selected_urls': urls,
                    'pages': [r for r, _ in documents], 'assets': list(self.assets.values()),
                    'failures': self.failures, 'runtime_review': self.runtime,
                    'limits': {k: getattr(self.args, k) for k in ('max_assets', 'max_file_mb', 'max_total_mb')}}
        self.write('asset-manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({'output': str(self.root), 'pages': len(documents), 'assets': len(self.assets), 'failures': len(self.failures), 'runtime_review': len(self.runtime)}, ensure_ascii=False))
        return 2 if self.failures else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', action='append', required=True, help='Exactly selected page URL; repeat for each approved page')
    parser.add_argument('--asset', action='append', default=[], help='Additional observed runtime resource URL')
    parser.add_argument('--output', required=True, help='New or empty output directory')
    parser.add_argument('--max-assets', type=int, default=600)
    parser.add_argument('--max-file-mb', type=float, default=64)
    parser.add_argument('--max-total-mb', type=float, default=256)
    args = parser.parse_args()
    if min(args.max_assets, args.max_file_mb, args.max_total_mb) <= 0:
        parser.error('Resource limits must be positive.')
    try:
        return Snapshot(args).run()
    except Exception as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
