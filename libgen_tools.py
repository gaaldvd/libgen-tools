# Handle search requests and manage results

from urllib.request import urlopen, urlretrieve
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

SOURCES = ("GET", "Cloudflare", "IPFS.io", "Infura", "Pinata")


def make_soup(url):

    # For easier soup making :)

    try:
        with urlopen(url) as page:
            html = page.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            return soup
    except (URLError, HTTPError) as cerr:
        raise ConnectionError("Connection error while making soup!") from cerr


class QueryError(Exception):

    # Raised when query is too short

    pass


class SearchRequest:  # Handling search request and returning results

    url_base = "https://www.libgen.is/search.php?column=def&req="

    def __init__(self, query=None):
        self.query = query
        if len(self.query) < 3:
            raise QueryError("Search string must contain"
                             "at least 3 characters!")
        self.request_url = f"{self.url_base}{self.query.replace(" ", "+")}"
        self.results = self.get_results()

    def get_results(self):
        table_raw = []  # BeautifulSoup objects
        table = []  # Contains the results as dictionaries
        soup = make_soup(self.request_url)
        result_count = int(soup.find_all('table')[1].text.split()[0])
        page_count = result_count // 25

        # Merging raw results from every page into table_raw
        pages = [soup.find_all('table')[2].find_all('tr')[1:]]
        if page_count > 1:
            for i in range(page_count):
                soup = make_soup(f"{self.request_url}&page={i + 2}")
                pages.append(soup.find_all('table')[2].find_all('tr')[1:])
        for page in pages:
            for row in page:
                table_raw.append(row)

        # Generating a list of dictionaries from table_raw
        for row in table_raw:
            columns = row.find_all('td')

            # Removing <i> tags from the Title column:
            i_tags = [tag.decompose() for tag in columns[2].find_all('i')]
            del i_tags

            entry = {'id': int(columns[0].text),
                     'auth': columns[1].text,
                     'title': columns[2].text,
                     'pub': columns[3].text,
                     'year': columns[4].text,
                     'pp': columns[5].text,
                     'lang': columns[6].text,
                     'size': columns[7].text,
                     'ext': columns[8].text}

            mirrors = [c.find('a')['href'] for c in columns[9:]
                       if c.find('a').text != "[edit]"]
            entry['mirrors'] = mirrors

            table.append(entry)

        return Results(table)


class Results:  # todo: filtering, status messages
    def __init__(self, results):
        self.entries = results

    def filter(self):

        # Filter by entry properties, return a list of entries

        pass

    def get_download_urls(self, entry):

        # Resolve links from mirrors

        try:
            soup = make_soup(entry['mirrors'][0])  # Mirror 1 by default
        except (URLError, HTTPError):
            print("Connection error while connecting to Mirror 1!")
        else:
            urls = [lnk['href'] for lnk in soup.find_all('a', string=SOURCES)]

        return urls

    def download(self, entry, path):

        # Download entry, default method is GET from the first mirror

        filename = f"{entry['id']}.{entry['ext']}"
        urls = self.get_download_urls(entry)
        for url in urls:
            try:
                urlretrieve(url, f"{path}/{filename}")
            except (URLError, HTTPError):
                print("Connection error while downloading!")
                continue
            else:
                break
