# libgen-tools TODO

## general

- docstrings

## test script

- parse arguments
- status messages insted of debug messages in libgen_tools module

## classes

### `SearchRequest(author, title)`

- `get_results(url)`: returns a Results object

### `Results()`

- `filter(properties...)`
  - called if there are active filters in the config file (default) or filtering is activated manually
- `get_download_urls(id)`
  - loop through mirrors (the method uses the first mirror by default)
    - http error 403 when making soup of mirror2 can be bypassed by [changing the user agent](https://stackoverflow.com/questions/24226781/changing-user-agent-in-python-3-for-urrlib-request-urlopen) ([some agents](https://www.zenrows.com/blog/user-agent-web-scraping#importance))
- `download(id)`

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
