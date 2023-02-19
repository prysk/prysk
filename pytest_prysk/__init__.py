try:
    import pytest
except ImportError as ex:
    error_msg = (
        "Pytest not available, "
        "make sure you install prysk using the extra [pytest-prysk].\n"
        "For further details, see also "
        "https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-extras"
    )
    raise Exception(error_msg) from ex

import os
from collections import ChainMap
from contextlib import contextmanager
from tempfile import TemporaryDirectory
from typing import (
    Iterable,
    Optional,
    Tuple,
    Union,
)

from _pytest._code import ExceptionInfo
from _pytest._code.code import TerminalRepr
from pytest import Collector
from pytest import Item as PytestItem

import prysk


@contextmanager
def environment(variables):
    old_env = os.environ.copy()
    os.environ.update(variables)
    yield os.environ
    os.environ = old_env


@contextmanager
def cwd(path):
    old_cwd = os.getcwd()
    os.chdir(path)
    yield path
    os.chdir(old_cwd)


_OPTIONS = {
    "shell": {
        "default": "/bin/sh",
        "type": str,
        "help": "Set the shell which will be used by prysk (default: %(default)s)",
    },
    "indent": {
        "default": 2,
        "type": int,
        "help": "Number of spaces to use for indentation (default: %(default)s)",
    },
}


def _envvar_name(name) -> str:
    return f"PRYSK_{name.upper()}"


def _option_name(name) -> str:
    return f"--prysk-{name.lower()}"


def _update_options(options):
    envvar_to_name = {_envvar_name(name): name for name in _OPTIONS}
    name_to_attribute_name = {
        name: f'prysk_{name.replace("-", "_")}' for name in _OPTIONS
    }

    cli_arguments = vars(options)
    cli_arguments = {
        attr_name: value
        for attr_name, value in cli_arguments.items()
        if attr_name in name_to_attribute_name.values() and value is not None
    }
    envvars = {
        name_to_attribute_name[envvar_to_name[envvar]]: _OPTIONS[
            envvar_to_name[envvar]
        ]["type"](value)
        for envvar, value in os.environ.items()
        if envvar in envvar_to_name and value is not None
    }
    defaults = {
        name_to_attribute_name[name]: value["default"]
        for name, value in _OPTIONS.items()
    }

    layered_options = ChainMap(cli_arguments, envvars, defaults)
    for name in (name_to_attribute_name[n] for n in _OPTIONS):
        setattr(options, name, layered_options[name])


class TestFailure(Exception):
    """A prysk test failure"""


def pytest_addoption(parser):
    group = parser.getgroup("prysk")
    for name, settings in _OPTIONS.items():
        kwargs = settings.copy()
        del kwargs["default"]
        group.addoption(_option_name(name), **kwargs)


def pytest_collect_file(parent, file_path):
    if prysk.test.is_testfile(file_path):
        return File.from_parent(parent, path=file_path)


class File(pytest.File):
    def collect(self) -> Iterable[Union[PytestItem, Collector]]:
        yield Item.from_parent(self, options=self.config.option, name=self.path.name)


class Item(pytest.Item):
    def __init__(self, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_marker("prysk")
        self.tmpdir = TemporaryDirectory()
        self.shell = options.prysk_shell
        self.indent = options.prysk_indent

    def setup(self) -> None:
        self.tmpdir.__enter__()

    def runtest(self) -> None:
        with cwd(self.tmpdir.name):
            variables = {"PRYSK_TEMP": self.tmpdir.name}
            with environment(variables):
                ins, outs, diff = prysk.test.testfile(
                    path=self.path, shell=self.shell, indent=self.indent
                )

        if outs is None and len(diff) == 0:
            pytest.skip("Process exited with return code 80")
        elif len(ins) == 0:
            pytest.skip("Test is empty")
        elif diff:
            raise TestFailure(diff)

    def teardown(self) -> None:
        self.tmpdir.__exit__(None, None, None)

    def repr_failure(
        self,
        excinfo: ExceptionInfo[BaseException],
        style: "Optional[_TracebackStyle]" = None,
    ) -> Union[str, TerminalRepr]:
        if excinfo.errisinstance(TestFailure):
            return b"".join(excinfo.value.args[0]).decode()
        return super().repr_failure(excinfo)

    def reportinfo(self) -> Tuple[Union["os.PathLike[str]", str], Optional[int], str]:
        return self.path, 0, f"[prysk] {self.name}"


def pytest_configure(config):
    config.addinivalue_line("markers", "prysk: mark test to be executed with prysk")
    _update_options(config.option)
