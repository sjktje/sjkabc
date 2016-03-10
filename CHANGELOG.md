# Change Log

## Unreleased

### Added

* Support for P: (parts)
* Tune method format_abc which returns a properly formatted tune.
* Support for F: (file)
* Support :: shorthand syntax (which equals :||:)
* strip_decorations()

### Removed

* Support for A: as it's deprecated according to the ABC standard.

### Fixed

* Travis-CI

## 1.1.0 - 2016-03-08

### Added

* The parser is now an iterable object (Parser) which yields Tune objects
* Lots of documentation

### Changed

* Documentation is now in ReST, generated with Sphinx.
* Some minor refactoring of code

### Fixed
