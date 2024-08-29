# libgen-tools TODO

## general

- temporary files: test.py, dummy.py, output.py, table (these are for development purposes)
- docstrings
- ISBN

## test script

- customize argument parsing
  - possible values in the help
- implement filtering
  - by args
  - by parsing filtering sequence

## classes

### `SearchRequest(query)`

- `get_results(url)`: returns a Results object

### `Results()`

- `filter_entries(filters)`
  - `filters = {'auth': "Author", 'ext': "Extension"}`
  - filtering by year: from-to
- `get_download_urls(entry)`
  - loop through mirrors (the method uses the first mirror by default)
    - http error 403 when making soup of mirror2 can be bypassed by [changing the user agent](https://stackoverflow.com/questions/24226781/changing-user-agent-in-python-3-for-urrlib-request-urlopen) ([some agents](https://www.zenrows.com/blog/user-agent-web-scraping#importance))
- `download(entry)`

Entries are stored in a list of dictionaries:

```python
entries = [{'id': 1234, 
            'auth': "Author", 
            'title': "Title", 
            'pub': "Publisher", 
            'year': "Year", 
            'pp': "Pages", 
            'lang': "Language", 
            'size': "Size", 
            'ext': "Extension", 
            'mirrors': ["url", "url"]}]
```
