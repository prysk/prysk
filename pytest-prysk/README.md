# Pytest-Prysk

With the `pytest-prysk` plugin, prysk tests can be executed using pytests.

This enables the usage of various pytests features like:

* The pytest test collection mechanisms
* Expression based test selection using the `-k` flag
* The pytest test reporting
* Making use of other [pytest plugins](https://docs.pytest.org/en/7.2.x/reference/plugin_list.html) like `pytest-xdist` for parallel test execution


## How to install the pytest plugin
In order to install prysk with pytest support, the extra **pytest-plugin**,
needs to be enabled. How this can be achieved depends or your package
management tool. Here are some examples:

* `pip install prysk-pytest`
* `poetry add pytest-prysk`


## How to run prysk tests with pytest

Once you installed the pytest-prysk plugin, it will use pytest mechanisms to collect your prysk tests.
So usually a simple `pytest` should do the trick.

Attention: In case you want to prevent pytest from running any prysk test just pass `-p no:prysk` to the pytest cli.

