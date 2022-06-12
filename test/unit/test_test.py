from pathlib import Path

import pytest

from prysk.test import TestFile, _findtests, cwd


def create_directory(root, name):
    _dir = Path(root) / name
    _dir.mkdir()
    return _dir


def create_file(directory, name, data):
    file = Path(directory) / name
    file.touch()
    with open(file, "w") as f:
        f.write(data)
    return file


def test_findtests_ignores_hidden_file_in_current_directory(tmpdir):
    file = create_file(tmpdir, "default.t", "")
    expected = (Path(file.name),)
    with cwd(tmpdir):
        assert tuple(_findtests([file.name])) == expected


def test_findtests_ignores_hidden_files(tmpdir):
    _ = create_file(tmpdir, ".hidden.t", "")
    visible_file = create_file(tmpdir, "visible.t", "")
    expected = (visible_file,)
    assert tuple(_findtests([tmpdir])) == expected


def test_findtests_ignores_folders(tmpdir):
    hidden_directory = create_directory(tmpdir, ".hidden")
    _ = create_file(hidden_directory, "visible.t", "")
    expected = tuple()
    assert tuple(_findtests([tmpdir])) == expected


class TestTestFile:
    def test_equivalent_test_files_have_the_same_hash(self):
        test_file1 = TestFile(".", None)
        test_file2 = TestFile(".", None)
        assert hash(test_file1) == hash(test_file2)

    @pytest.mark.parametrize(
        "file_path1, test_dir1, file_path2, test_dir2",
        [
            ("/some/file/path", None, "/another/file/path", None),
            ("/some/file/path", "/tmp", "/some/file/path", None),
        ],
    )
    def test_different_test_files_have_different_hashes(
        self, file_path1, test_dir1, file_path2, test_dir2
    ):
        test_file1 = TestFile(file_path1, test_dir1)
        test_file2 = TestFile(file_path2, test_dir2)
        assert hash(test_file1) != hash(test_file2)
