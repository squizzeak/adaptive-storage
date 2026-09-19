"""Regression checks for packaging completeness and isolation, not prompt wording."""
from pathlib import Path
import importlib.util
import shutil
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('distribution_build', ROOT / 'scripts/build.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        shutil.copytree(ROOT / 'skills', self.root / 'skills')
        shutil.copytree(ROOT / 'plugins', self.root / 'plugins')
        for name in ('LICENSE', 'PRIVACY.md'):
            shutil.copyfile(ROOT / name, self.root / name)
        module.build(self.root)

    def test_missing_setup_sibling_is_rejected(self):
        shutil.rmtree(self.root / 'skills/storage-init')
        with self.assertRaises(ValueError):
            module.build(self.root)

    def test_stale_bundle_is_detected_then_rebuilt(self):
        source = self.root / 'skills/adaptive-storage/references/setup.md'
        source.write_text(source.read_text() + '\nAdditional example.\n')
        with self.assertRaises(ValueError):
            module.build(self.root, check=True)
        module.build(self.root)
        module.build(self.root, check=True)

    def test_untracked_file_in_bundle_is_detected(self):
        (self.root / 'plugins/adaptive-storage/skills/private-note.md').write_text('not package data')
        with self.assertRaises(ValueError):
            module.build(self.root, check=True)

    def test_source_symlink_is_rejected(self):
        (self.root / 'skills/secret').symlink_to(self.root / 'LICENSE')
        with self.assertRaises(ValueError):
            module.build(self.root)

    def test_output_symlink_is_rejected_without_touching_target(self):
        target = self.root / 'user-data'
        target.mkdir()
        keep = target / 'keep.md'
        keep.write_text('preserve')
        output = self.root / 'plugins/adaptive-storage/skills'
        shutil.rmtree(output)
        output.symlink_to(target, target_is_directory=True)
        with self.assertRaises(ValueError):
            module.build(self.root)
        self.assertEqual(keep.read_text(), 'preserve')

    def test_archives_are_reproducible_and_complete(self):
        first, second = self.root / 'one.zip', self.root / 'two.zip'
        module.archive(self.root, first)
        module.archive(self.root, second)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as bundle:
            self.assertIsNone(bundle.testzip())
            names = set(bundle.namelist())
            for name in module.SKILLS:
                self.assertIn(f'adaptive-storage/skills/{name}/SKILL.md', names)
            self.assertIn('adaptive-storage/skills/adaptive-storage/references/setup.md', names)
            self.assertFalse(any('/.git/' in name or '/tests/' in name for name in names))

    def test_archive_does_not_overwrite(self):
        output = self.root / 'existing.zip'
        output.write_bytes(b'preserve')
        with self.assertRaises(FileExistsError):
            module.archive(self.root, output)
        self.assertEqual(output.read_bytes(), b'preserve')


if __name__ == '__main__':
    unittest.main()
