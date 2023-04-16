Development
-----------

The Repository
+++++++++++++++
Download the official development repository using Git_

.. code-block:: console

    git clone https://github.com/nicoretti/prysk.git

Visit GitHub_ if you'd like to fork the project, watch for new changes, or
report issues.

Dependencies
++++++++++++

In order to run all tests locally you need to have the following tools
installed.

Python
______
* python >= 3.7
* poetry

Shells
______
* dash
* bash
* zsh

If you have these dependencies all setup, just run a

.. code-block:: console

    poetry install


within the root folder of the project. Now you should be good to go!

Nox
++++
Mostly all task you will need to take care of are automated
using nox_. So if you want to run all checks and build
the documentation etc. just run:

.. code-block:: console

    nox

To get a list of all available targets run:

.. code-block:: console

    nox --list

For running a specific target run:

.. code-block:: console

    nox -s <target>

Creating a release
++++++++++++++++++
* Add a new empty `Unreleased` section to change log (**prysk_news.rst**)
* Rename the old Unreleased section to `Version <MAJOR>.<MINOR>.<PATCH> (<Month>. <Day>, <YEAR>)`
* Fine tune the change log / release notes
    - Add code snippets
    - Add examples
    - ...

* Update the version
    - Update the project version :code:`poetry version <major>.<minor>.<patch>`
    - Update the version number(s) in the code :code:`prysk.cli.VERSION`

* Validate the Project
    - Run checks
        * formatters
        * tests
        * linter(s)
        * etc.
    - Fix findings
        * fix findings
        * re-run checks

* Build artifacts
    - :code:`poetry build`

* Publish the Release
    - Release in SCM
        * Create git tag
            - :code:`git tag X.Y.Z`
        * Publish tag
            - :code:`git push origin x.Y.Z`
    - Release on GitHub
        * Publish a Github Release
            - :code:`gh release create --verify-tag <major>.<minor>.<patch>`
        * copy paste chang log information into the release
    - Release on PYPI
        * :code:`poetry publish`

* Check for Known Issues
    - Make sure gh-pages still work
        * A bug have been observed in cases where :code:`tag == master` is :code:`HEAD`.

.. _nox: https://nox.thea.codes/en/stable/
.. _Git: http://git-scm.com/
.. _GitHub: https://github.com/nicoretti/prysk
