## Usage

sjkabc provides a set of function that parses and manipulates ABC music notation. There are currently three basic types of functions:

* strip_* functions

    These functions return the passed string stripped from, for example, ornaments or accidentals. These can be used to create simplified notation that may suitable for searching.

* expand_* functions

    These functions will expand repeats, multiple endings, and 'long notes'. Suitable for creating more easily searchable abc for storing in a database.

* parse_* functions

    Used to parse plain text files containing abc. Can be used to slurp abc music into a database.


### strip_ornaments(abc)

Return abc stripped from ornaments like turns, trills, grace notes, fermatas and 'general ornaments' (~).

Example:

```python
>>> from sjkabc import strip_ornaments
>>> stripped = strip_ornaments('abc bcd|~c3 def|{/def}efg !trill(!abc|')
>>> stripped
'abc bcd|c3 def|efg abc|'
```

### strip_whitespace(abc)

Return abc stripped from whitespaces and newlines.

Example:

```python
>>> from sjkabc import strip_whitespace
>>> stripped = strip_whitespace('abc bcd | bcd cde | def efg |')
>>> stripped
'abcbcd|bcdcde|defefg|'
```

### strip_accidentals(abc)

Return abc stripped from accidentals.

Example:

```python
>>> from sjkabc import strip_accidentals
>>> stripped = strip_whitespace('abc ^c=de|_e^fg _g=fe')
>>> stripped
'abc cde|efg gfe'
```

### strip_octave(abc)

Return abc stripped from octave specifiers.

Example:

```python
>>> from sjkabc import strip_octave
>>> stripped = strip_octave("A,B,C,d'e'f'")
>>> stripped
'ABCdef'
```

### strip_bar_dividers(abc)

Return abc stripped from bar dividers.

Example:

```python
>>> from sjkabc import strip_bar_dividers
>>> stripped = strip_bar_dividers('abcd bcde|bcde abcd|defg abcd|bebe baba')
>>> stripped
'abcd bcdebcde abcddefg abcdbebe baba'
```

### strip_triplets(abc)

Return abc stripped from triplet (and duplet, quadruplets et.c.) markers. This function name is misleading and will probably be changed in a future release. In other words, triplets are ***not*** stripped, only the markers.

Example:

```python
>>> from sjkabc import strip_triplets
>>> stripped = strip_triplets('AB(3cBA Bcde|fd(3ddd (4efed (4BdBF')
>>> stripped
'ABcBA Bcde|fdddd efed BdBF'
```
### strip_chords(abc)

Return abc stripped from chords, both 'accompaniment' (i.e. "Gm") and multiple-note chords (i.e. \[GAbc\]).

Example:

```python
>>> from sjkabc import strip_chords
>>> stripped = strip_chords('"G" abc|"Em" bcd|[GBd] cde')
>>> stripped
' abc| bcd | cde'
```

### strip_extra_chars(abc)

Return abc stripped from the following characters:

* /
* \
* <
* \>


### expand_notes(abc)

Return abc where 'long notes' (a note with a digit) has been 'expanded', e.g. A2 -> AA.

Example:

```python
>>> from sjkabc import expand_notes
>>> expanded = expand_notes('A2cA FAE2|F3A dAcA')
>>> expanded
'AAcA FAEE|FFFA dAcA'
```
### expand_parts(abc)

Return abc where repeats and alternate endings have been expanded.

Example:


```python
>>> from sjkabc import expand_parts
>>> abc = 'A c/B/A {/d}AGE G3|A c/B/A {/d}AGE GED|A c/B/A {/d}AGE G2E|D F/E/D {/d}DEF GED:|'
>>> expanded = expand_parts(abc)
>>> expanded
'A c/B/A {/d}AGE G3|A c/B/A {/d}AGE GED|A c/B/A {/d}AGE G2E|D F/E/D {/d}DEF GED|A c/B/A {/d}AGE G3|A c/B/A {/d}AGE GED|A c/B/A {/d}AGE G2E|D F/E/D {/d}DEF GED|'
>>> abc = 'abc abc|cde cde|def def|1fga fga:|gab gab||'
>>> expanded = expand_parts(abc)
>>> expanded
'abc abc|cde cde|def def|fga fga|abc abc|cde cde|def def|gab gab||'
```

### expand_abc(abc)

Return string that has been processed with all above functions.

### parse_file(filename)

Parse file and yield dictionaries of tunes. Since some header items may occur multiple times (like T: for title), all dictionary items will consist of lists. The following ABC fields are currently supported

* A:area
* B:book
* C:composer
* D:discography
* G:group
* H:history
* I:instruction
* K:key
* L:note_length
* M:metre
* N:notes
* O:origin
* Q:tempo
* R:rhythm
* S:source
* T:title
* X:index
* Z:transcription


Example:

```python
>>> from sjkabc import parse_file
>>> for tune in parse_file('music/reels.abc')
>>> for tune in abc:
...     for title in tune['title']:
...         print(title)
...
In Memory Of Coleman
Apples In Winter
```

### parse_dir(dir)

Same as `parse_file()`, but works on all files ending with .abc in `dir` and subdirectories.
