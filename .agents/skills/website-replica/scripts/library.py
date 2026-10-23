#!/usr/bin/env python3
"""Serve the local template center and isolated, root-routed template previews."""
import argparse
from functools import partial
import html
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import re
import threading
from urllib.parse import parse_qs, quote, unquote, urlsplit
import webbrowser

SKILL = Path(__file__).resolve().parents[1]
TEMPLATES = SKILL / 'assets/templates'
CENTER = SKILL / 'assets/center'


def within(root, value):
    target = (root / value).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError('Path outside the selected directory')
    return target


def catalog():
    items = []
    for metadata in sorted(TEMPLATES.glob('*/template.json')):
        item = json.loads(metadata.read_text())
        slug = metadata.parent.name
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', slug):
            raise ValueError('Invalid template directory name: ' + slug)
        if not within(metadata.parent, item.get('entry', 'index.html')).is_file():
            raise ValueError('Missing template entry: ' + slug)
        cover = item.get('cover', '')
        if cover and not within(metadata.parent, cover).is_file():
            raise ValueError('Missing template cover: ' + slug)
        item.update({'id': slug, 'previewUrl': '/open/' + slug,
                     'coverUrl': '/templates/' + slug + '/' + quote(cover), 'learnUrl': '/learn/' + slug})
        items.append(item)
    return sorted(items, key=lambda item: (item.get('order', 100), item['name']))


class StaticHandler(SimpleHTTPRequestHandler):
    """Static preview with clean routes and byte ranges for original videos."""
    def log_message(self, fmt, *args):
        if args and str(args[1] if len(args) > 1 else '') not in ('200', '206', '304'):
            super().log_message(fmt, *args)

    def translate_path(self, path):
        result = Path(super().translate_path(path))
        root = Path(self.directory).resolve()
        if not result.resolve().is_relative_to(root):
            return str(root / '__not_found__')
        if result.is_dir() and (result / 'index.html').is_file():
            return str(result / 'index.html')
        if not result.exists() and not result.suffix and (result / 'index.html').is_file():
            return str(result / 'index.html')
        return str(result)

    def guess_type(self, path):
        if path.endswith(('.mjs', '.js')):
            return 'text/javascript'
        return super().guess_type(path)

    def send_head(self):
        path = Path(self.translate_path(self.path))
        if not path.is_file():
            return super().send_head()
        size = path.stat().st_size
        cms_range = parse_qs(urlsplit(self.path).query).get('range') if path.suffix == '.framercms' else None
        if cms_range:
            from io import BytesIO
            pieces = []
            for segment in cms_range[0].split(','):
                match = re.fullmatch(r'(\d+)-(\d+)', segment)
                if not match or int(match.group(1)) > int(match.group(2)) or int(match.group(2)) >= size:
                    self.send_error(416)
                    return None
                with path.open('rb') as stream:
                    stream.seek(int(match.group(1)))
                    pieces.append(stream.read(int(match.group(2)) - int(match.group(1)) + 1))
            data = b''.join(pieces)
            self._remaining = len(data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            return BytesIO(data)
        start, end = 0, size - 1
        range_header = self.headers.get('Range')
        if range_header:
            match = re.fullmatch(r'bytes=(\d*)-(\d*)', range_header.strip())
            if not match or not size or not any(match.groups()):
                self.send_error(416)
                return None
            left, right = match.groups()
            if left:
                start, end = int(left), min(int(right), size - 1) if right else size - 1
            else:
                start = max(0, size - int(right))
            if start > end or start >= size:
                self.send_response(416)
                self.send_header('Content-Range', 'bytes */' + str(size))
                self.end_headers()
                return None
        stream = path.open('rb')
        stream.seek(start)
        self._remaining = end - start + 1
        self.send_response(206 if range_header else 200)
        self.send_header('Content-Type', self.guess_type(str(path)))
        self.send_header('Content-Length', str(self._remaining))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Cache-Control', 'no-cache')
        if range_header:
            self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.end_headers()
        return stream

    def copyfile(self, source, output):
        remaining = getattr(self, '_remaining', None)
        if remaining is None:
            return super().copyfile(source, output)
        try:
            while remaining > 0:
                chunk = source.read(min(65536, remaining))
                if not chunk:
                    break
                output.write(chunk)
                remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass


class PreviewPool:
    def __init__(self):
        self.servers, self.lock = {}, threading.Lock()

    def url(self, slug, entry):
        with self.lock:
            if slug not in self.servers:
                server = ThreadingHTTPServer(('127.0.0.1', 0), partial(StaticHandler, directory=str(TEMPLATES / slug)))
                threading.Thread(target=server.serve_forever, daemon=True).start()
                self.servers[slug] = server
            port = self.servers[slug].server_port
        route = '/' if entry == 'index.html' else '/' + quote(entry)
        return f'http://127.0.0.1:{port}' + route

    def close(self):
        for server in self.servers.values():
            server.shutdown()
            server.server_close()


POOL = PreviewPool()


def markdown_view(source):
    """Small escaped document viewer; code and headings are enough for the guides."""
    blocks, paragraph, in_code = [], [], False
    def flush():
        if paragraph:
            blocks.append('<p>' + '<br>'.join(paragraph) + '</p>')
            paragraph.clear()
    for line in source.splitlines():
        if line.startswith('```'):
            flush()
            blocks.append('</code></pre>' if in_code else '<pre><code>')
            in_code = not in_code
        elif in_code:
            blocks.append(html.escape(line) + '\n')
        elif line.startswith('#'):
            flush()
            match = re.match(r'^(#{1,6})\s+(.*)', line)
            if match:
                level = len(match.group(1))
                blocks.append(f'<h{level}>' + html.escape(match.group(2)) + f'</h{level}>')
            else:
                paragraph.append(html.escape(line))
        elif not line.strip():
            flush()
        else:
            paragraph.append(html.escape(line))
    flush()
    if in_code:
        blocks.append('</code></pre>')
    return ''.join(blocks)


class CenterHandler(StaticHandler):
    def send_json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        try:
            items = catalog()
            by_id = {item['id']: item for item in items}
            if path == '/api/catalog':
                return self.send_json({'templates': items})
            if path.startswith('/open/'):
                slug = path.split('/')[2]
                if slug not in by_id:
                    return self.send_error(404)
                self.send_response(302)
                self.send_header('Location', POOL.url(slug, by_id[slug].get('entry', 'index.html')))
                self.end_headers()
                return
            if path.startswith('/learn/'):
                slug = path.split('/')[2]
                if slug not in by_id:
                    return self.send_error(404)
                item = by_id[slug]
                guide = within(TEMPLATES / slug, item.get('guide', 'STUDY_GUIDE.md'))
                text = guide.read_text() if guide.is_file() else '该模板暂未提供学习文档。'
                name = html.escape(item['name'])
                body = ('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                        '<title>' + name + ' · 学习指南</title><link rel="stylesheet" href="/center.css">'
                        '<body class="guide-page"><nav><a href="/">← 返回模板中心</a><a class="button" href="/open/' + slug + '" target="_blank">打开 ' + name + ' ↗</a></nav>'
                        '<main class="guide-document">' + markdown_view(text) + '</main></body></html>').encode()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            if path.startswith('/templates/'):
                pieces = path.split('/', 3)
                if len(pieces) != 4 or pieces[2] not in by_id:
                    return self.send_error(404)
                file = within(TEMPLATES / pieces[2], pieces[3])
                if not file.is_file():
                    return self.send_error(404)
                data = file.read_bytes()
                self.send_response(200)
                self.send_header('Content-Type', mimetypes.guess_type(str(file))[0] or 'application/octet-stream')
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            return super().do_GET()
        except (ValueError, json.JSONDecodeError) as error:
            self.send_error(400, str(error))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=4176)
    parser.add_argument('--open', action='store_true')
    parser.add_argument('--check', action='store_true', help='Validate template registrations without starting a server')
    args = parser.parse_args()
    if args.check:
        print(json.dumps({'templates': catalog()}, ensure_ascii=False, indent=2))
        return
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(CenterHandler, directory=str(CENTER)))
    print(f'Template center: http://127.0.0.1:{server.server_port}/', flush=True)
    print('Press Control+C to stop the center and its template previews.', flush=True)
    if args.open:
        webbrowser.open(f'http://127.0.0.1:{server.server_port}/')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        POOL.close()
        server.server_close()


if __name__ == '__main__':
    main()
