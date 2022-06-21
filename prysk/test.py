"""Utilities for running individual tests"""
import itertools
import os
import re
import time
from collections.abc import Iterable
from contextlib import contextmanager
from dataclasses import dataclass, field
from inspect import getmembers, ismethod
from pathlib import Path
from uuid import uuid4

from prysk.diff import esc, glob, regex, unified_diff
from prysk.process import PIPE, STDOUT, execute

__all__ = ["test", "testfile", "runtests"]

_SKIP = 80
_IS_ESCAPING_NEEDED = re.compile(rb"[\x00-\x09\x0b-\x1f\x7f-\xff]").search


def _escape(s):
    """Like the string-escape codec, but doesn't escape quotes"""
    escape_sub = re.compile(rb"[\x00-\x09\x0b-\x1f\\\x7f-\xff]").sub
    escape_map = dict((bytes([i]), rb"\x%02x" % i) for i in range(256))
    escape_map.update({b"\\": b"\\\\", b"\r": rb"\r", b"\t": rb"\t"})
    return escape_sub(lambda m: escape_map[m.group(0)], s[:-1]) + b" (esc)\n"


def _findtests(paths):
    """Yield tests in paths in sorted order"""

    paths = list(map(Path, paths))

    def is_hidden(path):
        """Check if a path (file/dir) is hidden or not."""

        def _is_hidden(part):
            return (
                    part.startswith(".")
                    and not part == "."
                    and not part.startswith("..")
                    and not part.startswith("./")
            )

        return any(map(_is_hidden, path.parts))

    def is_testfile(path):
        """Check if path is a valid prysk test file"""
        return path.is_file() and path.suffix == ".t" and not is_hidden(path)

    def is_test_dir(path):
        """Check if the path is a valid prysk test dir"""
        return path.is_dir() and not is_hidden(path)

    def remove_duplicates(path):
        """Stable duplication removal"""
        return list(dict.fromkeys(path))

    def collect(paths):
        """Collect all test files compliant with cram collection order"""
        for path in paths:
            if is_testfile(path):
                yield path
            if is_test_dir(path):
                yield from sorted((f for f in path.rglob("*.t") if is_testfile(f)))

    yield from remove_duplicates(collect(paths))


@contextmanager
def cwd(path):
    """Change the current working directory and restore it afterwards."""
    _cwd = os.getcwd()
    os.chdir(path)
    try:
        yield path
    finally:
        os.chdir(_cwd)


def test(
        lines,
        shell="/bin/sh",
        indent=2,
        testname=None,
        env=None,
        cleanenv=True,
        debug=False,
):
    r"""Run test lines and return input, output, and diff.

    This returns a 3-tuple containing the following:

        (list of lines in test, same list with actual output, diff)

    diff is a generator that yields the diff between the two lists.

    If a test exits with return code 80, the actual output is set to
    None and diff is set to [].

    Note that the TESTSHELL environment variable is available in the
    test (set to the specified shell). However, the TESTDIR and
    TESTFILE environment variables are not available. To run actual
    test files, see testfile().

    Example usage:

    >>> refout, postout, diff = test([b'  $ echo hi\n',
    ...                               b'  [a-z]{2} (re)\n'])
    >>> refout == [b'  $ echo hi\n', b'  [a-z]{2} (re)\n']
    True
    >>> postout == [b'  $ echo hi\n', b'  hi\n']
    True
    >>> bool(diff)
    False

    lines may also be a single bytes string:

    >>> refout, postout, diff = test(b'  $ echo hi\n  bye\n')
    >>> refout == [b'  $ echo hi\n', b'  bye\n']
    True
    >>> postout == [b'  $ echo hi\n', b'  hi\n']
    True
    >>> bool(diff)
    True
    >>> (b''.join(diff) ==
    ...  b'--- \n+++ \n@@ -1,2 +1,2 @@\n   $ echo hi\n-  bye\n+  hi\n')
    True

    :param lines: Test input
    :type lines: bytes or collections.Iterable[bytes]
    :param shell: Shell to run test in
    :type shell: bytes or str or list[bytes] or list[str]
    :param indent: Amount of indentation to use for shell commands
    :type indent: int
    :param testname: Optional test file name (used in diff output)
    :type testname: bytes or None
    :param env: Optional environment variables for the test shell
    :type env: dict or None
    :param cleanenv: Whether or not to sanitize the environment
    :type cleanenv: bool
    :param debug: Whether or not to run in debug mode (don't capture stdout)
    :type debug: bool
    return: Input, output, and diff iterables
    :rtype: (list[bytes], list[bytes], collections.Iterable[bytes])
    """
    indent = b" " * indent
    cmdline = indent + b"$ "
    conline = indent + b"> "
    salt = b"PRYSK%.5f" % time.time()

    def create_environment(environment, shell, clean=False):
        _env = os.environ.copy() if environment is None else environment
        _env["TESTSHELL"] = shell
        if clean:
            _env.update({key: "C" for key in ["LANG", "LC_ALL", "LANGUAGE"]})
            _env["TZ"] = "GMT"
            _env["CDPATH"] = ""
            _env["COLUMNS"] = "80"
            _env["GREP_OPTIONS"] = ""
        return _env

    lines = lines.splitlines(True) if isinstance(lines, bytes) else lines
    shell = [shell] if isinstance(shell, (bytes, str)) else shell
    env = create_environment(env, shell[0], clean=cleanenv)

    if debug:
        return _debug(cmdline, conline, env, lines, shell)

    after = {}
    refout, postout = [], []
    i = pos = prepos = -1
    stdin = []
    for i, line in enumerate(lines):
        if not line.endswith(b"\n"):
            line += b"\n"
        refout.append(line)
        if line.startswith(cmdline):
            after.setdefault(pos, []).append(line)
            prepos = pos
            pos = i
            stdin.append(b"echo %s %d $?\n" % (salt, i))
            stdin.append(line[len(cmdline):])
        elif line.startswith(conline):
            after.setdefault(prepos, []).append(line)
            stdin.append(line[len(conline):])
        elif not line.startswith(indent):
            after.setdefault(pos, []).append(line)
    stdin.append(b"echo %s %d $?\n" % (salt, i + 1))

    output, retcode = execute(
        shell + ["-"], stdin=b"".join(stdin), stdout=PIPE, stderr=STDOUT, env=env
    )
    if retcode == _SKIP:
        return refout, None, []

    pos = -1
    for i, line in enumerate(output[:-1].splitlines(True)):
        out, cmd = line, None
        if salt in line:
            out, cmd = line.split(salt, 1)

        if out:
            if not out.endswith(b"\n"):
                out += b" (no-eol)\n"

            if _IS_ESCAPING_NEEDED(out):
                out = _escape(out)
            postout.append(indent + out)

        if cmd:
            ret = int(cmd.split()[1])
            if ret != 0:
                postout.append(indent + b"[%d]\n" % ret)
            postout += after.pop(pos, [])
            pos = int(cmd.split()[0])

    postout += after.pop(pos, [])

    if testname:
        diff_path = bytes(testname)
        error_path = bytes(Path(testname.parent, f"{testname.name}.err"))
    else:
        diff_path = error_path = b""

    diff = unified_diff(
        refout, postout, diff_path, error_path, matchers=[esc, glob, regex]
    )
    for line in diff:
        return refout, postout, itertools.chain([line], diff)
    return refout, postout, []


def _debug(cmdline, conline, env, lines, shell):
    stdin = []
    for line in lines:
        if not line.endswith(b"\n"):
            line += b"\n"
        if line.startswith(cmdline):
            stdin.append(line[len(cmdline):])
        elif line.startswith(conline):
            stdin.append(line[len(conline):])
    execute(shell + ["-"], stdin=b"".join(stdin), env=env)
    return [], [], []


def testfile(
        path, shell="/bin/sh", indent=2, env=None, cleanenv=True, debug=False,
        testname=None
):
    """Run test at path and return input, output, and diff.

    This returns a 3-tuple containing the following:

        (list of lines in test, same list with actual output, diff)

    diff is a generator that yields the diff between the two lists.

    If a test exits with return code 80, the actual output is set to
    None and diff is set to [].

    Note that the TESTDIR, TESTFILE, and TESTSHELL environment
    variables are available to use in the test.

    :param path: Path to test file
    :type path: bytes or str
    :param shell: Shell to run test in
    :type shell: bytes or str or list[bytes] or list[str]
    :param indent: Amount of indentation to use for shell commands
    :type indent: int
    :param env: Optional environment variables for the test shell
    :type env: dict or None
    :param cleanenv: Whether or not to sanitize the environment
    :type cleanenv: bool
    :param debug: Whether or not to run in debug mode (don't capture stdout)
    :type debug: bool
    :param testname: Optional test file name (used in diff output)
    :type testname: bytes or None
    :return: Input, output, and diff iterables
    :rtype: (list[bytes], list[bytes], collections.Iterable[bytes])
    """
    with open(path, "rb") as f:
        abspath = path.resolve()
        env = env or os.environ.copy()
        env["TESTDIR"] = f"{abspath.parent}"
        env["TESTFILE"] = f"{abspath.name}"
        if testname is None:
            testname = path
        return test(
            f,
            shell,
            indent=indent,
            testname=testname,
            env=env,
            cleanenv=cleanenv,
            debug=debug,
        )


class LegacyRunner:
    def __init__(self, paths, tmpdir, settings):
        self._paths = paths
        self._tmpdir = tmpdir
        self._settings = settings

    def __iter__(self):
        def wrapper(t):
            return lambda: t(self._settings)

        return ((t.path, wrapper(t)) for t in self._test_files())

    def _test_files(self):
        for path in _findtests(self._paths):
            yield TestFile(path, self._tmpdir)


@dataclass(frozen=True)
class Settings:
    shell: list
    indent: int = 2
    debug: bool = False
    clean_environment: bool = True


class TestFile:
    def __init__(self, path, tmp_dir):
        self._file = path
        self._tmp_dir = tmp_dir

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def __hash__(self):
        return hash((self._file, self._tmp_dir))

    @property
    def path(self):
        return self._file

    def run(self, settings):
        """Run tests contained in this file yield result.

        Runs the test in a temporary directory and returns a 3-tuple:

            (list of lines in the test, same list with actual output, diff)
        """
        # if test file is empty return an empty result
        if not self._file.stat().st_size:
            return None, None, None

        directory = self._tmp_dir / self._file.name / f"{uuid4()}"
        directory.mkdir(parents=True)
        abspath = self._file.resolve()
        with cwd(directory):
            return testfile(
                abspath,
                settings.shell,
                indent=settings.indent,
                cleanenv=settings.clean_environment,
                debug=settings.debug,
                testname=self._file,
            )


class EventRegistry:
    def __init__(self, events):
        self._hooks = {event: [] for event in events}

    @property
    def events(self):
        return (event for event in self._hooks)

    def trigger(self, event, *args, **kwargs):
        """Triggers all hooks of the specified event."""
        for hook in self._hooks[event]:
            hook(*args, **kwargs)

    def register(self, plugin):
        """Registers a complex plugin which need to register for multiple events."""
        callables = ((name, member) for name, member in getmembers(plugin, ismethod))
        hooks = {name: member for name, member in callables if name in self._hooks}
        for event, hook in hooks.items():
            self[event] = hook

    def __getitem__(self, event):
        """Returns all listeners registered for a specific event."""
        return self._hooks[event]

    def __setitem__(self, event, value):
        """Adds one or multiple listeners for a specific event."""
        try:
            hooks = self._hooks[event]
        except KeyError as ex:
            raise KeyError(f"Unknown event [{event}]") from ex

        if isinstance(value, Iterable):
            hooks.extend(value)
        else:
            hooks.append(value)


class Runner:
    EVENTS = (
        "pre-run",
        "post-run",
        "pre-test",
        "post-test",
        "empty-test",
        "skipped-test",
        "succeeded-test",
        "failed-test",
    )

    def __int__(self, path, tmpdir, settings):
        self._event_registry = EventRegistry(self.EVENTS)

    def _test_files(self):
        for path in _findtests(self._paths):
            yield TestFile(path, self._tmpdir)

    def _trigger(self, event, *args, **kwargs):
        self._event_registry.trigger(event, *args, **kwargs)

    def add(self, plugin):
        self._event_registry.register(plugin)

    def run(self):
        self._trigger("pre-run")
        for test in self._test_files():
            self.execute(test)
        self._trigger("post-run")

    def execute(self, test):
        self._trigger("pre-test")
        refout, postout, diff = test()
        if refout is None:
            self._trigger("empty-test")
        if postout is None:
            self._trigger("skipped-test")
        elif not diff:
            self._trigger("succeeded-test")
        else:
            self._trigger("failed-test")
        self._trigger("post-test")

