#!/usr/bin/env python3
"""Behavioral regression checks against an isolated, local HTTP fixture.

Run: python3 <skill-dir>/scripts/test_snapshot.py
No live reference site, browser, or third-party dependency is required.
"""
import argparse
import base64
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest

from audit import audit
from snapshot import Document, Snapshot, srcset_parts


class Fixture(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.seen.append(self.path)
        if self.path == '/landing':
            self.send_response(302)
            self.send_header('Location', '/nested/home')
            self.end_headers()
            return
        record = self.server.files.get(self.path)
        if record is None:
            self.send_response(404)
            self.end_headers()
            return
        ctype, body = record
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.end_headers()
        self.wfile.write(body.encode() if isinstance(body, str) else body)

    def log_message(self, *args):
        pass


class SnapshotBehavior(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'replica'
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Fixture)
        self.server.seen, self.server.files = [], {}
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.origin = 'http://127.0.0.1:' + str(self.server.server_port)
        self.runtime = b'window.example = "Keep this exact script byte sequence";'
        self.sri = 'sha256-' + base64.b64encode(hashlib.sha256(self.runtime).digest()).decode()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def add(self, path, content_type, body):
        self.server.files[path] = (content_type, body)

    def run_snapshot(self, pages, **overrides):
        args = argparse.Namespace(url=[self.origin + p for p in pages], asset=[], output=str(self.root),
                                  max_assets=600, max_file_mb=64, max_total_mb=256)
        for key, value in overrides.items():
            setattr(args, key, value)
        return Snapshot(args).run()

    def document(self, path='index.html'):
        return Document((self.root / path).read_text(), 'https://local-replica.invalid/' + path)

    def test_scope_fragments_assets_css_sri_and_scripts(self):
        self.add('/', 'text/html', '''<!doctype html><html><head><meta charset="utf-8">
          <link rel="stylesheet" href="/css/site.css" integrity="old-css-hash">
          <script src="/runtime.js" integrity="SRI"></script>
          <script>const originalUrl = "/images/same.svg";</script></head><body>
          <a id="menu" href="#">Menu</a><a id="panel" href="#panel">Panel</a>
          <a id="inside" href="/about?mode=one#details">Inside</a>
          <a href="/not-in-scope">Not selected</a><a href="/about?mode=two">Other query</a>
          <img src="/images/same.svg" srcset="/images/same.svg 1x, /other/same.svg 2x">
          <img src="/image-transform?width=640&amp;quality=80">
          <svg><use href="/images/same.svg#arrow"></use></svg>
          <video data-poster-url="/poster.jpg" data-video-urls="/video.mp4,/video.webm" style="background-image:url(&quot;/poster.jpg&quot;)">
            <source src="/video.mp4"></video>
          <iframe src="https://example.test/embed"></iframe>
          <form action="/submit"><input type="email" required></form>
          </body></html>'''.replace('SRI', self.sri))
        self.add('/about?mode=one', 'text/html', '<html><head></head><body><a href="/#top">Home</a></body></html>')
        self.add('/css/site.css', 'text/css', '@import "theme.css"; body{background:url("../images/same.svg#paint")} @font-face{font-family:x;src:url("../fonts/font.woff2?v=2")}')
        self.add('/css/theme.css', 'text/css', 'i{background:url(../other/same.svg)}')
        self.add('/runtime.js', 'application/javascript', self.runtime)
        for path in ('/images/same.svg', '/other/same.svg'):
            self.add(path, 'image/svg+xml', '<svg xmlns="http://www.w3.org/2000/svg"/>')
        for path in ('/poster.jpg', '/video.mp4', '/video.webm', '/fonts/font.woff2?v=2', '/image-transform?width=640&quality=80'):
            self.add(path, 'application/octet-stream', b'fixture-data')
        self.assertEqual(self.run_snapshot(['/', '/about?mode=one']), 0)
        self.assertNotIn('/not-in-scope', self.server.seen)
        self.assertNotIn('/about?mode=two', self.server.seen)
        self.assertNotIn('/submit', self.server.seen)
        document = self.document()
        ids = {n['attrs'].get('id'): n['attrs'] for n in document.nodes}
        self.assertEqual(ids['menu']['href'], '#')
        self.assertEqual(ids['panel']['href'], '#panel')
        self.assertTrue(ids['inside']['href'].startswith('pages/'))
        self.assertTrue(ids['inside']['href'].endswith('#details'))
        styles = [n for n in document.nodes if n['tag'] == 'link']
        self.assertNotIn('integrity', styles[0]['attrs'])
        script = next(n for n in document.nodes if n['tag'] == 'script' and n['attrs'].get('integrity'))
        self.assertEqual(script['attrs']['integrity'], self.sri)
        self.assertEqual((self.root / script['attrs']['src']).read_bytes(), self.runtime)
        self.assertIn('const originalUrl = "/images/same.svg";', document.source)
        sprite = next(n for n in document.nodes if n['tag'] == 'use')
        self.assertTrue(sprite['attrs']['href'].endswith('#arrow'))
        manifest = json.loads((self.root / 'asset-manifest.json').read_text())
        same_names = [a['path'] for a in manifest['assets'] if a['url'].endswith('/same.svg')]
        self.assertEqual(len(set(same_names)), 2)
        self.assertEqual(manifest['failures'], [])
        result = audit(self.root)
        self.assertEqual(result['missing'], [])
        self.assertEqual(result['hash_mismatches'], [])
        self.assertTrue(any(e['kind'] == 'embed' for e in result['external']))
        # Missing assets and altered bytes must be detectable after a successful capture.
        resource = self.root / same_names[0]
        resource.write_text('modified')
        self.assertIn(same_names[0], audit(self.root)['hash_mismatches'])
        resource.unlink()
        self.assertTrue(audit(self.root)['missing'])

    def test_redirect_base_and_relative_urls(self):
        self.add('/nested/home', 'text/html', '<html><head><base href="/cdn/"><link rel="stylesheet" href="style"></head><body><img src="image"><a href="#">Menu</a><a href="../other">Outside</a></body></html>')
        self.add('/cdn/style', 'text/css', 'b{background:url(image)}')
        self.add('/cdn/image', 'image/png', b'png-fixture')
        self.assertEqual(self.run_snapshot(['/landing']), 0)
        doc = self.document()
        base = next(n for n in doc.nodes if n['tag'] == 'base')
        self.assertNotIn('href', base['attrs'])
        self.assertIn('/cdn/style', self.server.seen)
        self.assertIn('/cdn/image', self.server.seen)
        self.assertEqual(audit(self.root)['missing'], [])

    def test_partial_failures_and_existing_output(self):
        self.add('/', 'text/html', '<html><head></head><body><img src="/missing.png"></body></html>')
        self.assertEqual(self.run_snapshot(['/']), 2)
        manifest = json.loads((self.root / 'asset-manifest.json').read_text())
        self.assertEqual(len(manifest['failures']), 1)
        self.assertIn(self.origin + '/missing.png', (self.root / 'index.html').read_text())
        original = (self.root / 'index.html').read_bytes()
        with self.assertRaises(ValueError):
            self.run_snapshot(['/'])
        self.assertEqual((self.root / 'index.html').read_bytes(), original)

    def test_limits_report_incomplete_output(self):
        self.add('/', 'text/html', '<html><head></head><body><img src="/large"></body></html>')
        self.add('/large', 'image/png', b'x' * 8192)
        self.assertEqual(self.run_snapshot(['/'], max_file_mb=0.001), 2)
        failures = json.loads((self.root / 'asset-manifest.json').read_text())['failures']
        self.assertTrue(any('max-file-mb' in f['error'] for f in failures))

    def test_srcset_data_url_and_cli(self):
        self.assertEqual(srcset_parts('data:image/svg+xml;base64,PHN2Zz4= 1x, /large.png 2x'),
                         [('data:image/svg+xml;base64,PHN2Zz4=', '1x'), ('/large.png', '2x')])
        self.add('/', 'text/html', '<html><head></head><body>CLI fixture</body></html>')
        result = subprocess.run([sys.executable, str(Path(__file__).with_name('snapshot.py')),
                                 '--url', self.origin + '/', '--output', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run([sys.executable, str(Path(__file__).with_name('audit.py')),
                                 '--root', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / 'qa/static-audit.json').is_file())

    def test_encoded_resource_paths_and_no_document_preload_crawl(self):
        self.add('/', 'text/html', '<html><head><link rel="preload" as="document" href="/outside"></head><body><img src="/media/头像 one.svg"><img src="/media/encoded%2Fslash.svg"></body></html>')
        self.add('/media/%E5%A4%B4%E5%83%8F%20one.svg', 'image/svg+xml', '<svg/>')
        self.add('/media/encoded%2Fslash.svg', 'image/svg+xml', '<svg/>')
        self.assertEqual(self.run_snapshot(['/']), 0)
        self.assertNotIn('/outside', self.server.seen)
        self.assertIn('/media/encoded%2Fslash.svg', self.server.seen)
        self.assertEqual(audit(self.root)['missing'], [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
