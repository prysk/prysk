# Prysk

## Snapshot Testing

| Project        | Subdirectory             | Description                       | Badges                                                                                                                                                      |
|----------------|--------------------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Prysk          | [prysk]()          | The Prysk project                 | [![PyPI Version](https://img.shields.io/pypi/v/prysk)](https://pypi.org/project/prysk/) [![Downloads](https://img.shields.io/pypi/dm/prysk)](https://pypi.org/project/prysk/) [![Python Version](https://img.shields.io/pypi/pyversions/prysk)](https://pypi.org/project/prysk/) |
| Pytest Plugin  | [pytest-prysk]()   | The pytest plugin                 | [![PyPI Version](https://img.shields.io/pypi/v/pytest-prysk)](https://pypi.org/project/pytest-prysk/) [![Downloads](https://img.shields.io/pypi/dm/pytest-prysk)](https://pypi.org/project/pytest-prysk/) [![Python Version](https://img.shields.io/pypi/pyversions/pytest-prysk)](https://pypi.org/project/pytest-prysk/) |
| Prysk Website  | [website]()        | The project website for Prysk     |                                                                                                                                                             |

## Overview

Prysk is a fork of the popular snapshot testing tool [Cram](https://bitheap.org/cram). Even though Cram is pretty complete and mature for everyday use, Prysk wants to continue pushing its development forward.

Prysk tests look like snippets of interactive shell sessions. Prysk runs each command and compares the command output in the test with the command's actual output.

Here's a snippet from [Prysk's own test suite](https://github.com/Nicoretti/prysk/blob/master/test/integration/prysk/usage.t):


### Example Output

```diff
.s.!
--- examples/fail.t
+++ examples/fail.t.err
@@ -3,21 +3,22 @@
   $ echo 1
   1
   $ echo 1
-  2
+  1
   $ echo 1
   1

 Invalid regex:

   $ echo 1
-  +++ (re)
+  1

 Offset regular expression:

   $ printf 'foo\nbar\nbaz\n\n1\nA\n@\n'
   foo
+  bar
   baz

   \d (re)
   [A-Z] (re)
-  #
+  @
s.
```
```console
# Ran 6 tests, 2 skipped, 1 failed.
```

For more details see prysk's [README](prysk/README.rst) or checkout the [documentation]().
