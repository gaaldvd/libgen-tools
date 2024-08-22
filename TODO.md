# libgen-tools TODO

## general

- resolve download links when Requests.download() is called and on selection of entry in GUI mode
- basic information in every py file (usage, GitHub links, contact, etc.)
- test.py for demonstration
- convert debug outputs into status messages where it's useful
- docstrings

## classes

### `SearchRequest(author, title)`

- `get_results(url)`: returns a Results object

<div align="justify">
It is unclear if the class should take author and title as separate parameters or the query as a single string, because filtering based on author will be implemented by the filter() method of the Results class.
When entering a query in the GUI/CLI, the concatenated string (author+title) can be passed as a parameter to the SearchRequest class and the Author input field or argument (if filled) is used as a parameter for filtering.
For now, the class takes two separate parameters (author and title).
</div>

### `Results()`

- `filter(properties...)`: returns a new Results object
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
