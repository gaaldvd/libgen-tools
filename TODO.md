# libgen-tools TODO

## general

- temporary files: test.py, debug.py, dummy.py, table (these are for development purposes)
- docstrings
- ISBN

### implementation-merging workflow:

- `debug`
  - `test`
    - `libgen_tools`
  - `libgen_tools`

## test script

- customize argument helps
  - possible values for [language](https://www.iso.org/iso-639-language-code)
  - extension: djvu, epub, mobi, pdf, zip (...)
- filtering
  - implement validation for language and extension

## classes

### `SearchRequest(query)`

- `query, request_url, results`

- methods
  - `get_results(url)` returns a Results object

### `Results()`

- `entries` are stored in a list of dictionaries:

```python
entries = [{'id': 1234,
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

- methods
  - `filter_entries(filters)`
    - `filters = {'auth': "Author", 'ext': "Extension"}`
  - `get_download_urls(entry)`
    - raise ConnectionError (handle it in test script)?
    - loop through mirrors (the method uses the first mirror by default)
      - http error 403 when making soup of mirror2 can be bypassed by [changing the user agent](https://stackoverflow.com/questions/24226781/changing-user-agent-in-python-3-for-urrlib-request-urlopen) ([some agents](https://www.zenrows.com/blog/user-agent-web-scraping#importance))
  - `download(entry)`
    - raise ConnectionError (handle it in test script)?
