Pytest-Plugin
==============
Prysk optionally can be installed with pytest support. If the user chooses to do so,
various features and benefits provided by pytest and its plugins will be also available
for the prysk tests.

E.g.:

* The pytest test collection mechanisms
* Expression based test selection using the :code:`-k` flag
* The test reporting of pytest
* Parallel test execution (using pytest-xdist)
* `And a lot more <https://docs.pytest.org/en/7.2.x/reference/plugin_list.html>`_

How to install the pytest plugin
--------------------------------
In order to install prysk with pytest support, the extra **pytest-plugin**,
needs to be enabled. How this can be achieved depends or your package
management tool. Here are some examples:

* :code:`pip install 'prysk[pytest-plugin]'`
* :code:`poetry add -E "pytest-plugin" prysk`


How to run prysk tests with pytest
----------------------------------
Once you installed prysk with pytest, it will use pytest mechanisms to collect your prysk tests.
So usually a simple :code:`pytest` does the trick.

.. attention::

    In case you want to prevent pytest from running any prysk test just pass :code:`-p no:prysk` to the pytest cli.
