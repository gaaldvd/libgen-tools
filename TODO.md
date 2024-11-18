# libgen-tools TODO

## general

- packaging: move files to package in distribution phase
- temporary files: test.py, debug.py, dummy.py, table (these are for development purposes)
- default path for download()
- package docstrings
- developer notes to readme
  - technical documentation from docstrings

### implementation-merging workflow:

- `debug`
  - `test`
    - `libgen_tools`
  - `libgen_tools`

## test script

## classes

### `SearchRequest(query)`

- `query, request_url, raw_results, results`

- methods
  - `get_results(url)` returns a raw table as a list of BeautifulSoup objects
  - `create_entry_list(table)` returns a list of SEDs

### `Results(results)`

- `entries` are stored in a list of SEDs

- methods
  - `filter_entries(filters)`
  - `get_download_urls(entry)`
    - raise ConnectionError (handle it in test script)
    - loop through mirrors (the method uses the first mirror by default)
      - http error 403 when making soup of mirror2 can be bypassed by [changing the user agent](https://stackoverflow.com/questions/24226781/changing-user-agent-in-python-3-for-urrlib-request-urlopen) ([some agents](https://www.zenrows.com/blog/user-agent-web-scraping#importance))
  - `download(entry)`
    - raise ConnectionError (handle it in test script)
