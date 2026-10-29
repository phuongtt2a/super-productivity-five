#!/usr/bin/env python3
"""Package Five as the four-file ZIP expected by Super Productivity.

Usage: python scripts/package.py [--output dist/five-super-productivity.zip]
       python scripts/package.py --tag v1.0.1
No third-party dependencies.
"""
import argparse
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugin'
FILES = ('manifest.json', 'plugin.js', 'index.html', 'icon.svg')


def build(output: Path, tag: str | None = None) -> Path:
    manifest = json.loads((PLUGIN / 'manifest.json').read_text(encoding='utf-8'))
    assert manifest.get('manifestVersion') == 1, 'Invalid manifest version'
    assert manifest.get('iFrame') is True, 'Missing iframe support'
    assert manifest.get('id') == 'sp-top-5-today', 'Changing ID would break existing synced selections'
    assert re.fullmatch(r'\d+\.\d+\.\d+', manifest.get('version', '')), 'Invalid semantic version'
    if tag and tag != 'v' + manifest['version']:
        raise ValueError(f'Release tag {tag!r} must match manifest v{manifest["version"]}')
    if sorted(f.name for f in PLUGIN.iterdir() if f.is_file()) != sorted(FILES):
        raise ValueError('The plugin folder must contain precisely the four expected files')
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for filename in FILES:
            content = (PLUGIN / filename).read_bytes()
            item = zipfile.ZipInfo(filename, (2026, 1, 1, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o644 << 16
            z.writestr(item, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(output) as z:
        assert z.namelist() == list(FILES) and z.testzip() is None
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist' / 'five-super-productivity.zip')
    parser.add_argument('--tag', help='Optional GitHub tag, e.g. v1.0.1')
    args = parser.parse_args()
    print(build(args.output.resolve(), args.tag))
