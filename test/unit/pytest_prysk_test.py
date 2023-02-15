import os

from pytest_prysk import (
    cwd,
    environment,
)


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


def test_update_options():
    pass
    # priority
