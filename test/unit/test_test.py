from pathlib import Path

from prysk.test import (
    _findtests,
    cwd,
)


def create_directory(root, name):
    _dir = Path(root) / name
    _dir.mkdir()
    return _dir


def create_file(directory, name, data):
    file = Path(directory) / name
    file.write_text(data)
    return file


def test_findtests_ignores_hidden_file_in_current_directory(tmp_path):
    file = create_file(tmp_path, "default.t", "")
    expected = (Path(file.name),)
    with cwd(tmp_path):
        assert tuple(_findtests([file.name])) == expected


def test_findtests_ignores_hidden_files(tmp_path):
    _ = create_file(tmp_path, ".hidden.t", "")
    visible_file = create_file(tmp_path, "visible.t", "")
    expected = (visible_file,)
    assert tuple(_findtests([tmp_path])) == expected


def test_findtests_ignores_folders(tmp_path):
    hidden_directory = create_directory(tmp_path, ".hidden")
    _ = create_file(hidden_directory, "visible.t", "")
    expected = tuple()
    assert tuple(_findtests([tmp_path])) == expected
