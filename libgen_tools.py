# Handle search requests and manage results

from urllib.request import urlopen
from bs4 import BeautifulSoup


class SearchRequest:

    url_base = "https://www.libgen.is/search.php?column=def&req="

    def __init__(self, author=None, title=None):
        self.author = author
        self.title = title
        if author and title:
            self.request_url = f"{self.url_base}{author.replace(" ", "+")}+{title.replace(" ", "+")}"
        elif author:
            self.request_url = f"{self.url_base}{author.replace(" ", "+")}"
        elif title:
            self.request_url = f"{self.url_base}{title.replace(" ", "+")}"

    pass


class Entry:
    pass


class Results:
    pass
