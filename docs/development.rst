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

* Commit and publish changes as release preparation

* Trigger the Release

    In order to trigger a release a new tag must be pushed to Github.
    For further details see: `.github/workflows/ci-cd.yml`.


    #. Create a local tag with the appropriate version number

        .. code-block:: shell

            git tag x.y.z

    #. Push the tag to Github

        .. code-block:: shell

            git push origin x.y.z

What to do if the release failed?
_________________________________

The release failed during pre-release checks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Delete the local tag

    .. code-block:: shell

        git tag -d x.y.z

#. Delete the remote tag

    .. code-block:: shell

        git push --delete origin x.y.z

#. Fix the issue(s) which lead to the failing checks
#. Start the release process from the beginning


One of the release steps failed (Partial Release)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#. Check the Github action/workflow to see which steps failed
#. Finish or redo the failed release steps manually

.. note:: Example

    **Scenario**: Publishing of the release on Github was successfully but during the PyPi release, the upload step got interrupted.

    **Solution**: Manually push the package to PyPi


.. _nox: https://nox.thea.codes/en/stable/
.. _Git: http://git-scm.com/
.. _GitHub: https://github.com/nicoretti/prysk
