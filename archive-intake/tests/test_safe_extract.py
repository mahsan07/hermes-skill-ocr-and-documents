import importlib.util
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

MODULE = Path(__file__).parents[1] / "scripts" / "safe_extract.py"
spec = importlib.util.spec_from_file_location("safe_extract", MODULE)
safe_extract = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(safe_extract)


class SafeExtractTests(unittest.TestCase):
    def test_preserves_structure_and_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            z = root / "bundle.zip"
            with zipfile.ZipFile(z, "w") as out:
                out.writestr("a/b.txt", "hello")
                out.writestr("c.txt", "world")
            dest = root / "out"
            entries = safe_extract.inspect_zip(z, 200.0)
            safe_extract.enforce_limits(entries, 100, 10_000, 10_000)
            safe_extract.extract_zip(z, dest)
            m = safe_extract.manifest(z, dest, entries)
            self.assertEqual((dest / "a/b.txt").read_text(), "hello")
            self.assertEqual((dest / "c.txt").read_text(), "world")
            self.assertEqual(m["file_count"], 2)

    def test_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as td:
            z = Path(td) / "bad.zip"
            with zipfile.ZipFile(z, "w") as out:
                out.writestr("../escape.txt", "nope")
            with self.assertRaises(ValueError):
                safe_extract.inspect_zip(z, 200.0)

    def test_rejects_zip_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            z = Path(td) / "link.zip"
            info = zipfile.ZipInfo("link")
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            with zipfile.ZipFile(z, "w") as out:
                out.writestr(info, "target")
            with self.assertRaises(ValueError):
                safe_extract.inspect_zip(z, 200.0)


if __name__ == "__main__":
    unittest.main()
