import os
import shutil
from inspect import cleandoc

import pytest

from pytest_prysk import cwd, environment

pytest_plugins = "pytester"


def test_environment_contex_manager_adds_variables():
    env_vars = {"FOO": "BAR"}
    with environment(env_vars) as env:
        for var in env_vars:
            assert var in env


def test_environment_context_manager_restores_environment():
    old_env = os.environ.copy()
    env_vars = {"FOO": "BAR"}
    with environment(env_vars):
        pass
    assert old_env == os.environ


def test_cwd_context_manager_changes_current_working_directory(tmp_path):
    with cwd(tmp_path) as path:
        assert f"{path}" == os.getcwd()


def test_cwd_context_manager_restores_current_working_directory(tmp_path):
    old_cwd = os.getcwd()
    with cwd(tmp_path):
        pass
    assert old_cwd == os.getcwd()


def test_option_has_valid_default_value(pytester):
    expected_indent = 2
    expected_shell = "/bin/sh"
    config = pytester.parseconfigure()
    options = config.option
    assert (
        expected_indent == options.prysk_indent
        and expected_shell == options.prysk_shell
    )


def test_option_env_setting_takes_precedence_over_default(pytester):
    expected_shell = "/bin/zsh"
    expected_indent = 4

    env = pytester._monkeypatch
    env.setenv("PRYSK_SHELL", expected_shell)
    env.setenv("PRYSK_INDENT", f"{expected_indent}")

    config = pytester.parseconfigure()
    options = config.option
    assert (
        expected_indent == options.prysk_indent
        and expected_shell == options.prysk_shell
    )


def test_option_cli_parameter_takes_precedence_over_env(pytester):
    expected_shell = "/bin/bash"
    expected_indent = 5

    env = pytester._monkeypatch
    env.setenv("PRYSK_SHELL", "/bin/zsh")
    env.setenv("PRYSK_INDENT", "3")

    config = pytester.parseconfigure(
        f"--prysk-shell={expected_shell}", f"--prysk-indent={expected_indent}"
    )
    options = config.option
    assert (
        expected_indent == options.prysk_indent
        and expected_shell == options.prysk_shell
    )


def test_failed_test_is_reported(pytester):
    pytester.makefile(
        ".t",
        cleandoc(
            """
        Smoke test
          $ echo Foo
          Invalid Expectation
        """
        ),
    )
    result = pytester.runpytest()
    assert result.ret == pytest.ExitCode.TESTS_FAILED


def test_successful_test_is_reported(pytester):
    pytester.makefile(
        ".t",
        cleandoc(
            """
        Smoke test
          $ echo Foo
          Foo
        """
        ),
    )
    result = pytester.runpytest()
    assert result.ret == pytest.ExitCode.OK


def test_no_test_files_found(pytester):
    result = pytester.runpytest()
    assert result.ret == pytest.ExitCode.NO_TESTS_COLLECTED


def test_regression_github_issue_169(pytester):
    prysk_file = pytester.makefile(
        ".t",
        # fmt: off
        cleandoc(
            """
            Smoke test
              $ echo Foo
              Foo
            """
            # fmt: on
        ),
    )
    python_file = pytester.makefile(
        ".py",
        cleandoc(
            # fmt: off
            '''
            from os import (
                environ,
                pathsep,
            )

            def extend_path():
                """
                >>> from os import environ
                >>> expected = "/this/is/just/a/unique/entry"
                >>> expected in environ['PATH']
                False
                >>> extend_path()
                >>> expected in environ['PATH']
                True
                """
                environ["PATH"] += pathsep + "/this/is/just/a/unique/entry"
            '''
            # fmt: on
        ),
    )

    # we need to make sure the prysk test is executed before the doctest in order to trigger the bug
    prysk_tests = pytester.mkdir("a")
    python_tests = pytester.mkdir("z")
    # shutil.move in python 3.8 has issue when passing posix paths
    shutil.move(str(prysk_file), str(prysk_tests))
    shutil.move(str(python_file), str(python_tests))

    result = pytester.runpytest("--doctest-modules")
    assert result.ret == pytest.ExitCode.OK
