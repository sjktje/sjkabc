Change Log
==========

1.4.0 (2016-06-21)
------------------

* format_abc() wraps header lines prefixing them with '+:'.

1.3.1 (2016-04-23)
------------------

* format_abc() will not include empty header lines.

1.3.0 (2016-03-27)
------------------

* Added support for continued info field lines (+:)
* Added factories for testing
* Unittest replaced with pytest
* Tune.format_abc() will no longer include empty info fields
* Add strip_slurs() which removes slurs (parentheses) from string. This function is called by expand_abc.

1.2.2 (2016-03-11)
------------------

* Fixed bug introduced by the Tune.abc and Tune.expanded_abc changes in last release
  This bug broke Tune.format_abc()

1.2.1 (2016-03-10)
------------------

* Fixed bug which caused Tune.expanded_abc never to be set

1.2.0 (2016-03-10)
------------------

* Added support for P: (parts)
* Added tune method format_abc which returns a properly formatted tune
* Added support for F: (file)
* Added support :: shorthand syntax (which equals :||:)
* Added strip_decorations()
* Added strip_gracenotes()
* Removed support for A: as it's deprecated according to the ABC standard
* Fixed Travis-CI setup
* The strip_ornaments is now deprecated. It has been replaced by strip_decorations and strip_gracenotes and will be removed in future versions.

1.1.0 (2016-03-08)
------------------

* The parser is now an iterable object (Parser) which yields Tune objects
* Added lots of documentation
* Documentation is now in ReST, generated with Sphinx.
* Some minor refactoring of code
