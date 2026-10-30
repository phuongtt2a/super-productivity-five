"""Cheap tests that need only the Python standard library."""
from pathlib import Path
import json
import tempfile
import unittest
import zipfile
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from package import build, FILES

class PackageTests(unittest.TestCase):
    def test_manifest_and_authorship(self):
        m=json.loads((ROOT/'plugin/manifest.json').read_text())
        self.assertEqual(m['name'],'Five')
        self.assertEqual(m['author'],'phuongtt2a')
        self.assertEqual(m['id'],'sp-top-5-today')
        self.assertIn('getTasks',m['permissions'])
        self.assertIn('addTask',m['permissions'])
        self.assertIn('updateTask',m['permissions'])
        self.assertIn('persistDataSynced',m['permissions'])

    def test_zip_root_is_exactly_four_files(self):
        with tempfile.TemporaryDirectory() as temp:
            out=build(Path(temp)/'five.zip',tag='v1.0.5')
            with zipfile.ZipFile(out) as z:
                self.assertEqual(z.namelist(),list(FILES))
                self.assertIsNone(z.testzip())
                self.assertEqual(json.loads(z.read('manifest.json'))['name'],'Five')

    def test_tag_version_must_match(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                build(Path(temp)/'five.zip',tag='v0.0.0')

    def test_readme_screenshots_and_version_are_consistent(self):
        manifest=json.loads((ROOT/'plugin/manifest.json').read_text())
        self.assertEqual(manifest['version'],'1.0.5')
        readme=(ROOT/'README.md').read_text()
        import re
        shots=re.findall(r'docs/screenshots/[a-z-]+-v1\.0\.5\.webp',readme)
        self.assertGreaterEqual(len(set(shots)),3)
        for shot in set(shots):
            self.assertTrue((ROOT/shot).exists(),shot)

    def test_ui_has_core_controls(self):
        html=(ROOT/'plugin/index.html').read_text()
        for item in ('Arrange Five','data-drop-index','data-drag-selected','data-drag-task','data-move','id="create-form"','id="focus-list"','id="sort"'):
            self.assertIn(item,html)

if __name__ == '__main__':unittest.main()
