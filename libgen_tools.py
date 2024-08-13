# Handle search requests and manage results

from urllib.request import urlopen
from bs4 import BeautifulSoup


def make_soup(url):  # For easier soup making :)
    page = urlopen(url)
    html = page.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup


class QueryError(Exception):  # Raised when query is too short or no author nor title was entered
    pass


class SearchRequest:  # Handling search request and returning results

    url_base = "https://www.libgen.is/search.php?column=def&req="

    def __init__(self, author=None, title=None):
        self.author = author if author else ""
        self.title = title if title else ""
        if len(self.author + self.title) < 3:
            raise QueryError("Error: search string must contain at least 3 characters!")
        self.request_url = f"{self.url_base}{self.author.replace(" ", "+")}+{self.title.replace(" ", "+")}"

    def get_results(self):
        table_raw = []  # BeautifulSoup objects
        table = []  # contains the search results as dictionaries, returned as a Results object
        soup = make_soup(self.request_url)
        result_count = int(soup.find_all('table')[1].text.split()[0])
        page_count = (result_count // 25)

        # Merging raw results from every page into table_raw
        pages = [soup.find_all('table')[2].find_all('tr')[1:]]
        if page_count > 1:
            for i in range(page_count):
                soup = make_soup(f"{self.request_url}&page={i + 2}")
                pages.append(soup.find_all('table')[2].find_all('tr')[1:])
        for page in pages:
            [table_raw.append(row) for row in page]

        # Generating a list of dictionaries from table_raw
        for row in table_raw:
            columns = row.find_all('td')
            i_tags = columns[2].find_all('i')  # removing <i> tags from the Title column
            [i.decompose() for i in i_tags]
            table.append(
                {'id': columns[0].text,
                 'auth': columns[1].text,
                 'title': columns[2].text,
                 'pub': columns[3].text,
                 'year': columns[4].text,
                 'pp': columns[5].text,
                 'lang': columns[6].text,
                 'size': columns[7].text,
                 'ext': columns[8].text,
                 'mirror1': columns[9].find('a')['href'],  # todo: list of mirrors
                 'mirror2': columns[10].find('a')['href']})

        return table  # todo: return a Results object


class Results:
    def __init__(self):
        pass

    def filter(self):  # Filter by entry properties, return a filtered list of entries
        pass

    def download(self):  # Download by ID, default method is GET
        pass
