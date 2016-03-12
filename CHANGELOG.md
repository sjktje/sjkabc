# Change Log

## Unreleased

### Added

* Support for continued info field lines (+:).

## 1.2.2 - 2016-03-11

### Fixed

* Bug introduced by the Tune.abc and Tune.expanded_abc changes in last release.
  This bug broke Tune.format_abc().

## 1.2.1 - 2016-03-10

### Fixed

* Bug which caused Tune.expanded_abc never to be set.

## 1.2.0 - 2016-03-10

### Added

* Support for P: (parts)
* Tune method format_abc which returns a properly formatted tune.
* Support for F: (file)
* Support :: shorthand syntax (which equals :||:)
* strip_decorations()
* strip_gracenotes()

### Removed

* Support for A: as it's deprecated according to the ABC standard.

### Fixed

* Travis-CI

### Deprecated

* strip_ornaments. It has been replaced by strip_decorations and strip_gracenotes and will be removed in future versions.

## 1.1.0 - 2016-03-08

### Added

* The parser is now an iterable object (Parser) which yields Tune objects
* Lots of documentation

### Changed

* Documentation is now in ReST, generated with Sphinx.
* Some minor refactoring of code
