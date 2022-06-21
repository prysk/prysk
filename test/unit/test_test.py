from pathlib import Path

import pytest

from prysk.test import EventRegistry, TestFile, _findtests, cwd


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


class TestEventRegistry:
    def test_create_registry(self):
        events = ["on_start", "on_failure", "on_success"]
        registry = EventRegistry(events)
        assert list(events) == list(registry.events)

    def test_registering_hook_for_unknown_event_fails(self):
        events = ["on_start", "on_failure", "on_success"]
        registry = EventRegistry(events)

        with pytest.raises(KeyError) as execinfo:
            registry["on_test"] = lambda: "test hook"
        assert "Unknown event" in f"{execinfo.value}"

    def test_register_a_single_hook(self):
        hook = lambda: None
        events = ["on_start"]
        registry = EventRegistry(events)
        registry["on_start"] = hook

        assert hook in list(registry["on_start"])

    def test_register_a_multiple_hooks_at_once(self):
        hooks = [lambda: None, lambda: 1, lambda: 2]
        events = ["on_start"]
        registry = EventRegistry(events)
        registry["on_start"] = hooks
        expected = set(hooks)
        actual = set(registry["on_start"])

        assert expected == actual

    def test_register_for_multiple_events_using_a_class_based_listener(self):
        class Plugin:
            def on_success(self):
                pass

            def on_failure(self):
                pass

        plugin = Plugin()
        events = ["on_success", "on_failure"]
        registry = EventRegistry(events)
        registry.register(plugin)

        assert plugin.on_success in set(
            registry["on_success"]
        ) and plugin.on_failure in set(registry["on_failure"])
