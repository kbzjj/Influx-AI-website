#!/usr/bin/env python3
"""Exercise the center's preview/data flow with isolated temporary templates."""
from functools import partial
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import library


class LibraryFlow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old = library.TEMPLATES, library.CENTER, library.POOL
        library.TEMPLATES = Path(self.temp.name) / 'templates'
        library.CENTER = Path(self.temp.name) / 'center'
        library.CENTER.mkdir()
        (library.CENTER / 'index.html').write_text('Template center fixture')
        library.POOL = library.PreviewPool()
        self.add_template('one')
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), partial(library.CenterHandler, directory=str(library.CENTER)))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.origin = f'http://127.0.0.1:{self.server.server_port}'

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        library.POOL.close()
        library.TEMPLATES, library.CENTER, library.POOL = self.old
        self.temp.cleanup()

    def add_template(self, slug):
        root = library.TEMPLATES / slug
        (root / 'features').mkdir(parents=True)
        (root / 'index.html').write_text('HOME ' + slug)
        (root / 'features/index.html').write_text('FEATURES ' + slug)
        (root / 'cover.png').write_bytes(b'cover')
        (root / 'sample.mp4').write_bytes(b'0123456789')
        (root / 'data.framercms').write_bytes(b'ABCDEFGHIJKLMN')
        (root / 'STUDY_GUIDE.md').write_text('# Guide\n\n<script>unsafe</script>')
        (root / 'template.json').write_text(json.dumps({'name': slug, 'entry': 'index.html', 'cover': 'cover.png', 'sourceUrl': 'https://example.com/'}))

    def test_new_registrations_appear_without_restart(self):
        with urlopen(self.origin + '/api/catalog') as response:
            self.assertEqual(len(json.load(response)['templates']), 1)
        self.add_template('two')
        with urlopen(self.origin + '/api/catalog') as response:
            self.assertEqual(len(json.load(response)['templates']), 2)
        with urlopen(self.origin + '/templates/two/cover.png') as response:
            self.assertEqual(response.read(), b'cover')

    def test_cover_opens_root_preview_and_clean_route(self):
        with urlopen(self.origin + '/open/one') as response:
            self.assertEqual(response.read(), b'HOME one')
            preview = response.geturl().rstrip('/')
        self.assertNotEqual(preview, self.origin)
        with urlopen(preview + '/features') as response:
            self.assertEqual(response.geturl(), preview + '/features')
            self.assertEqual(response.read(), b'FEATURES one')
        with urlopen(self.origin + '/open/one') as response:
            self.assertEqual(response.geturl().rstrip('/'), preview)

    def test_video_and_cms_range_responses(self):
        with urlopen(self.origin + '/open/one') as response:
            preview = response.geturl().rstrip('/')
        with urlopen(Request(preview + '/sample.mp4', headers={'Range': 'bytes=2-5'})) as response:
            self.assertEqual(response.status, 206)
            self.assertEqual(response.headers['Content-Range'], 'bytes 2-5/10')
            self.assertEqual(response.read(), b'2345')
        with urlopen(preview + '/data.framercms?range=0-2,7-9') as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.read(), b'ABCHIJ')
        with self.assertRaises(HTTPError) as error:
            urlopen(preview + '/data.framercms?range=99-100')
        self.assertEqual(error.exception.code, 416)

    def test_guide_is_escaped_and_paths_stay_inside_template(self):
        with urlopen(self.origin + '/learn/one') as response:
            source = response.read().decode()
            self.assertIn('<h1>Guide</h1>', source)
            self.assertIn('&lt;script&gt;unsafe&lt;/script&gt;', source)
            self.assertNotIn('<script>unsafe', source)
        with self.assertRaises(HTTPError) as error:
            urlopen(self.origin + '/templates/one/%2e%2e/%2e%2e/secret.txt')
        self.assertEqual(error.exception.code, 400)
        metadata = library.TEMPLATES / 'one/template.json'
        item = json.loads(metadata.read_text())
        item['cover'] = '../outside.png'
        metadata.write_text(json.dumps(item))
        with self.assertRaises(ValueError):
            library.catalog()


if __name__ == '__main__':
    unittest.main(verbosity=2)
