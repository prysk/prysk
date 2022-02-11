Version 0.11.0 (February. 11, 2022)
-----------------------------------------------------
* Reorder publishing steps
* Fix release notes of 0.10.0 release

Version 0.10.0 (February. 11, 2022)
-----------------------------------------------------
* Add version sanity check
* Add support for automated releases
* Add support for retrieving project version from pyproject.toml

Version 0.9.0 (February. 11, 2022)
-----------------------------------------------------
* Add support for automated releases
* Add support for retrieving project version from pyproject.toml

Version 0.9 (Jan. 29, 2022)
---------------------------
* Add basic documentation
* Release new version to account and cope with accidentally
  deleted (untagged prysk version 0.8)

    .. note::
        once a version is published on pipy it can't be
        reused even if it has been deleted
        (see `file name reuse <https://pypi.org/help/#file-name-reuse>`_).

Version 0.8 (Jan. 25, 2022)
---------------------------
* Rename cram to prysk

    .. warning::
        Also semantically relevant names have been renamed,
        e.g. env var CRAMTMP is now PRYSK_TEMP
