from inspect import cleandoc
from pathlib import Path

import nox
from nox import Session

BASEPATH = Path(__file__).parent.resolve()
DOCS = BASEPATH / "docs"
BUILD = DOCS / "_build"

nox.options.sessions = [
    "clean",
    "isort",
    "code_format",
    "pylint",
    "mypy",
    "unit",
    "integration",
    "coverage",
    "docs",
]


@nox.session(python=False)
def clean(_: Session) -> None:
    coverage_file = BASEPATH / ".coverage"
    coverage_file.unlink(missing_ok=True)


@nox.session(python=False)
def fix(session: Session) -> None:
    session.run("poetry", "run", "python", "-m", "isort", "-v", f"{BASEPATH}")
    session.run("poetry", "run", "python", "-m", "black", f"{BASEPATH}")


@nox.session(python=False)
def code_format(session: Session) -> None:
    session.run(
        "poetry",
        "run",
        "python",
        "-m",
        "black",
        "--check",
        "--diff",
        "--color",
        f"{BASEPATH}",
    )


@nox.session(python=False)
def isort(session: Session) -> None:
    session.run(
        "poetry", "run", "python", "-m", "isort", "-v", "--check", f"{BASEPATH}"
    )


@nox.session(python=False)
def pylint(session: Session) -> None:
    session.run("poetry", "run", "python", "-m", "pylint", f'{BASEPATH / "prysk"}')
    session.run("poetry", "run", "python", "-m", "pylint", f'{BASEPATH / "scripts"}')


@nox.session(python=False)
def unit(session: Session) -> None:
    session.env["COVERAGE"] = "coverage"
    session.env["COVERAGE_FILE"] = f'{BASEPATH / ".coverage"}'
    session.run(
        "poetry",
        "run",
        "coverage",
        "run",
        "-a",
        f'--rcfile={BASEPATH / "pyproject.toml"}',
        "-m",
        "pytest",
        "-v",
        "-p",
        "no:prysk",
        "--doctest-modules",
        f"{BASEPATH}",
    )


@nox.session(python=False)
@nox.parametrize("shell", ["dash", "bash", "zsh"])
def integration(session: Session, shell: str) -> None:
    session.env["TESTOPTS"] = f"--shell={shell}"
    session.env["COVERAGE"] = "coverage"
    session.env["COVERAGE_FILE"] = f'{BASEPATH / ".coverage"}'
    session.run(
        "poetry",
        "run",
        "coverage",
        "run",
        "-a",
        f'--rcfile={BASEPATH / "pyproject.toml"}',
        "-m",
        "prysk",
        f"--shell={shell}",
        f'{BASEPATH / "test" / "integration"}',
        external=True,
    )


@nox.session(python=False)
def mypy(session: Session) -> None:
    session.run(
        "poetry",
        "run",
        "mypy",
        "--strict",
        "--show-error-codes",
        "--pretty",
        "--show-column-numbers",
        "--show-error-context",
        "--scripts-are-modules",
    )


@nox.session(python=False)
def coverage(session: Session) -> None:
    session.env["COVERAGE"] = "coverage"
    session.env["COVERAGE_FILE"] = f'{BASEPATH / ".coverage"}'
    session.run("coverage", "report", "--fail-under=97")
    session.run("coverage", "lcov")


@nox.session(python=False)
def docs(session: Session) -> None:
    session.run("sphinx-build", f"{DOCS}", f"{BUILD}")


@nox.session(name="multi-version-docs", python=False)
def multi_version_docs(session: Session) -> None:
    session.run("sphinx-multiversion", f"{DOCS}", f"{BUILD}")
    with open(BUILD / "index.html", "w") as f:
        f.write(
            cleandoc(
                """
              <!DOCTYPE HTML>
              <html lang="en-US">
              <head>
                  <meta charset="UTF-8">
                  <meta http-equiv="refresh" content="0; url=master/index.html">
                  <title>Page Redirection</title>
              </head>
              <body>
                  <!-- Note: don't tell people to `click` the link, just tell them that it is a link. -->
                  If you are not redirected automatically, follow this <a href='master/index.html'>Documentation</a>.
              </body>
              """
            )
        )
