# Changelog

## [Unreleased]

### Added
* Support for importing rack-types. (#180) (@bastianleicht)
* `--replace-existing-images` flag to prevent unnecessary image overwrites; the script now skips existing images by default. (#108) (@qspark-eliezerlp)
* ruff for code formatting and linting.

### Changed

* Switched to uv for dependency management.
* Upgraded Python version in Docker to 3.14.
* Improved `slug_format` based on Django slugify
* Replaced `os.path` and `glob` usage with `pathlib`.
* Replaced `datetime` with `time` for logging elapsed time.
* Use context manager for opening files in `upload_images`.

### Removed

* Support for Netbox versions older than 4.1.

### Fixed

* `KeyError: 'slug'` when attempting to filter items without slugs using the `--slugs` argument. (#117) (@jgroom33)
* Filter names for Netbox 4.1. (#152) (@chatasos)
* Upgraded `pynetbox` to fix various issues. (#134, #135, #142, #153, #163, #164)
* `urllib3` SSL warnings not being suppressed when `IGNORE_SSL_ERRORS` was set.
* `SyntaxWarning` regarding invalid escape sequences in Python 3.12+. (#139)
* Removed the strict `.git` suffix requirement for repos and set encoding to UTF-8 when opening. (#129, #161)
* `UnboundLocalError` when a parent object fails to create. (#133, #168, #169)
