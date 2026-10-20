"""Automated unittest suite for Task 3 Automated File Organizer."""

import tempfile
import unittest
from pathlib import Path

from task3_file_organizer.categories import CategoryMapper
from task3_file_organizer.organizer import organize_directory
from task3_file_organizer.safety_guard import (
    resolve_collision_path,
    validate_target_directory,
)


class TestCategoryMapper(unittest.TestCase):
    """Verify file extension categorization against taxonomy."""

    def setUp(self) -> None:
        self.mapper = CategoryMapper()

    def test_document_extensions(self) -> None:
        self.assertEqual(self.mapper.get_category("report.pdf"), "Documents")
        self.assertEqual(self.mapper.get_category("notes.txt"), "Documents")
        self.assertEqual(self.mapper.get_category("thesis.docx"), "Documents")

    def test_image_extensions(self) -> None:
        self.assertEqual(self.mapper.get_category("photo.jpg"), "Images")
        self.assertEqual(self.mapper.get_category("icon.png"), "Images")
        self.assertEqual(self.mapper.get_category("vector.svg"), "Images")

    def test_code_extensions(self) -> None:
        self.assertEqual(self.mapper.get_category("script.py"), "Code")
        self.assertEqual(self.mapper.get_category("app.js"), "Code")
        self.assertEqual(self.mapper.get_category("schema.json"), "Code")

    def test_other_unsupported_extensions(self) -> None:
        self.assertEqual(self.mapper.get_category("unknown.xyz123"), "Other")
        self.assertEqual(self.mapper.get_category("no_extension_file"), "Other")


class TestSafetyGuard(unittest.TestCase):
    """Verify protection of roots, system folders, and the project directory."""

    def test_reject_nonexistent_directory(self) -> None:
        is_safe, _ = validate_target_directory(Path("C:/non_existent_folder_99999"))
        self.assertFalse(is_safe)

    def test_reject_filesystem_root(self) -> None:
        is_safe, _ = validate_target_directory(Path("C:/"))
        self.assertFalse(is_safe)

    def test_reject_project_root(self) -> None:
        proj_dir = Path(__file__).resolve().parent.parent.parent
        is_safe, msg = validate_target_directory(proj_dir)
        self.assertFalse(is_safe)
        self.assertIn("refusing to organize", msg.lower())

    def test_collision_rename_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            existing = tmp / "document.pdf"
            existing.write_text("existing content")

            should_move, new_path = resolve_collision_path(existing, policy="rename")
            self.assertTrue(should_move)
            self.assertEqual(new_path.name, "document_1.pdf")

    def test_collision_skip_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            existing = tmp / "document.pdf"
            existing.write_text("existing content")

            should_move, path = resolve_collision_path(existing, policy="skip")
            self.assertFalse(should_move)


class TestOrganizerSandbox(unittest.TestCase):
    """Verify live directory organization, dry-run neutrality, and recursion prevention."""

    def test_dry_run_does_not_move_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            file1 = tmp / "test.pdf"
            file2 = tmp / "picture.png"
            file1.write_text("pdf content")
            file2.write_text("png content")

            code, res = organize_directory(tmp, dry_run=True)
            self.assertEqual(code, 0)
            self.assertEqual(res.scanned, 2)
            self.assertEqual(res.moved, 2)

            # Assert files were NOT actually moved
            self.assertTrue(file1.exists())
            self.assertTrue(file2.exists())
            self.assertFalse((tmp / "Documents").exists())
            self.assertFalse((tmp / "Images").exists())

    def test_live_move_categorizes_correctly(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            (tmp / "doc1.pdf").write_text("pdf")
            (tmp / "img1.png").write_text("png")
            (tmp / "song.mp3").write_text("mp3")
            (tmp / "data.csv").write_text("csv")

            code, res = organize_directory(tmp, dry_run=False)
            self.assertEqual(code, 0)
            self.assertEqual(res.moved, 4)

            self.assertTrue((tmp / "Documents" / "doc1.pdf").exists())
            self.assertTrue((tmp / "Images" / "img1.png").exists())
            self.assertTrue((tmp / "Audio" / "song.mp3").exists())
            self.assertTrue((tmp / "Spreadsheets" / "data.csv").exists())

    def test_rerun_does_not_reorganize_subfolders(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            (tmp / "sample.pdf").write_text("pdf")

            # First run: moves into Documents/
            organize_directory(tmp, dry_run=False)
            self.assertTrue((tmp / "Documents" / "sample.pdf").exists())

            # Second run: should scan 0 top-level files and skip the Documents directory
            code, res2 = organize_directory(tmp, dry_run=False)
            self.assertEqual(code, 0)
            self.assertEqual(res2.scanned, 0)
            self.assertEqual(res2.moved, 0)
            self.assertTrue(res2.skipped >= 1)


if __name__ == "__main__":
    unittest.main()
