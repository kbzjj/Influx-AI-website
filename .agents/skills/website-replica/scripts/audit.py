#!/usr/bin/env python3
"""Audit a localized static snapshot without executing site code or fetching URLs."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import quote, unquote, urljoin, urlsplit

from snapshot import Document, css_refs, node_resources


ORIGIN = 'https://local-replica.invalid/'


def audit(root):
    root = Path(root).resolve()
    missing, changed, external, routes, checked = [], [], [], [], set()
    manifest_path = root / 'asset-manifest.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    def records(value):
        if isinstance(value, dict):
            return [({'url': url, 'path': item} if isinstance(item, str) else {'url': url, **item}) for url, item in value.items()]
        return value
    assets = records(manifest.get('assets', []))
    pages = records(manifest.get('pages', []))

    def check(value, base, source, kind='resource'):
        if not value.strip() or value.startswith('#'):
            return
        url = urljoin(base, value)
        parsed = urlsplit(url)
        if parsed.scheme not in ('http', 'https'):
            return
        record = {'source': source, 'kind': kind, 'url': url}
        if parsed.netloc != urlsplit(ORIGIN).netloc:
            external.append(record)
            return
        path = (root / unquote(parsed.path).lstrip('/')).resolve()
        if not path.is_relative_to(root):
            missing.append({**record, 'reason': 'reference escapes output directory'})
            return
        if path.is_dir():
            path /= 'index.html'
        if not path.is_file():
            if kind == 'navigation' and not path.suffix:
                routes.append(record)
            else:
                missing.append({**record, 'path': str(path.relative_to(root))})
        else:
            checked.add(str(path.relative_to(root)))

    for path in sorted(root.rglob('*.html')):
        relative = str(path.relative_to(root))
        if path.relative_to(root).parts[0] in ('_source', 'qa'):
            continue
        doc = Document(path.read_text(encoding='utf-8'), ORIGIN + quote(relative))
        for node in doc.nodes:
            for value in node_resources(node):
                check(value, doc.base, relative)
            if node['tag'] in ('a', 'area', 'iframe'):
                value = node['attrs'].get('src' if node['tag'] == 'iframe' else 'href')
                if value:
                    check(value, doc.base, relative, 'embed' if node['tag'] == 'iframe' else 'navigation')
        for _, _, data in doc.styles:
            for value in css_refs(data):
                check(value, doc.base, relative, 'inline-css')

    for path in sorted(root.rglob('*.css')):
        relative = str(path.relative_to(root))
        if path.relative_to(root).parts[0] in ('_source', 'qa'):
            continue
        for value in css_refs(path.read_text(encoding='utf-8')):
            check(value, ORIGIN + quote(relative), relative, 'css')

    for record in assets:
        path = (root / record['path']).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            missing.append({'source': 'asset-manifest.json', 'path': record['path']})
        elif record.get('sha256') and hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
            changed.append(record['path'])
    for record in pages:
        path = (root / record['path']).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            missing.append({'source': 'asset-manifest.json', 'path': record['path']})

    # Avoid repeating identical lazy-load/srcset references in the report.
    def unique(records):
        return list({json.dumps(r, sort_keys=True): r for r in records}.values())

    return {'local_files_checked': len(checked), 'manifest_assets_checked': len(assets),
            'missing': unique(missing), 'hash_mismatches': changed, 'external': unique(external),
            'runtime_routes': unique(routes), 'download_failures': manifest.get('failures', []),
            'runtime_review': manifest.get('runtime_review', []),
            'note': 'Static checks only. External embeds, JS modules, API calls and visual/motion fidelity require browser verification.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        parser.error('Snapshot directory does not exist.')
    result = audit(root)
    report = root / 'qa/static-audit.json'
    report.parent.mkdir(exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'report': str(report), 'files_checked': result['local_files_checked'],
                      'missing': len(result['missing']), 'changed_assets': len(result['hash_mismatches']),
                      'external': len(result['external']), 'runtime_review': len(result['runtime_review'])}, ensure_ascii=False))
    return 2 if result['missing'] or result['hash_mismatches'] or result['download_failures'] else 0


if __name__ == '__main__':
    sys.exit(main())
