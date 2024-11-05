# libgen-tools

**A Python library for downloading content from [Library Genesis](https://libgen.is/).**

The library serves as a backend for [libgenx](https://github.com/gaaldvd/libgenx), a GUI/CLI application for using [LibGen](https://libgen.is/), but it is available for implementation in any other Python project as well.

*Under development.*

- Update (Nov, 2024): Documenting phase.
- Update (Aug, 2024): LibGen feels ill these days, this slows down development a bit.

## Installation

## Requirements

- [Python 3+](https://www.python.org/downloads/)
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)

## Usage

After installing from pip, import the library to your Python script:

`import libgentools`

or

`from libgentools import SearchRequest, Results, ...`

### Classes

#### SearchRequest

The class handles search requests and generates a list of results.

A new instance can be created with the `query` parameter:

`request = SearchRequest('principles of geology')`

The `request.results` variable now holds the search results as a list of Standard Entry Dictionaries (SEDs).

*Standard Entry Dictionary*:

```python
entries = [{'id': 1234,
            'isbn': ["ISBN", "ISBN"],
            'auth': "Author",
            'title': "Title",
            'pub': "Publisher",
            'year': 1999,
            'pp': "Pages",
            'lang': "Language",
            'size': "Size",
            'ext': "Extension",
            'mirrors': ["url", "url"]}]
```

A new `Results` instance can be constructed from the `request.results` variable:

`results = Results(request.results)`

#### Results

### Exceptions

### QueryError

### FilterError

## Reporting errors

Any error can be reported through [e-mail](mailto:gaaldavid[at]tuta.io?subject=[GitHub]%20libgen-tools%20error) with the exact error message and/or console screenshot.
