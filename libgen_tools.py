# Handle search requests and manage results

from urllib.request import urlopen, urlretrieve
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

SOURCES = ("GET", "Cloudflare", "IPFS.io", "Infura", "Pinata")


def make_soup(url):

    # For easier soup making :)

    with urlopen(url) as page:
        html = page.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        return soup


class QueryError(Exception):

    # Raised when query is too short or no author nor title was entered

    pass


class SearchRequest:  # Handling search request and returning results

    url_base = "https://www.libgen.is/search.php?column=def&req="

    def __init__(self, query=None):
        self.query = query
        if len(self.query) < 3:
            raise QueryError("Error: search string must"
                             "contain at least 3 characters!")

        self.request_url = f"{self.url_base}{self.query.replace(" ", "+")}"

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
            [table_raw.append(row) for row in page]

        # Generating a list of dictionaries from table_raw
        for row in table_raw:
            mirrors = []
            columns = row.find_all('td')

            # Removing <i> tags from the Title column:
            i_tags = columns[2].find_all('i')
            [tag.decompose() for tag in i_tags]

            entry = {'id': int(columns[0].text),
                     'auth': columns[1].text,
                     'title': columns[2].text,
                     'pub': columns[3].text,
                     'year': columns[4].text,
                     'pp': columns[5].text,
                     'lang': columns[6].text,
                     'size': columns[7].text,
                     'ext': columns[8].text}

            # The list of possible mirrors:
            [mirrors.append(c.find('a')['href'])
             for c in columns[9:] if c.find('a').text != "[edit]"]
            entry['mirrors'] = mirrors

            table.append(entry)

        results = Results(table)
        return results


class Results:  # todo: filtering, status messages
    def __init__(self, results):
        self.entries = results

    def filter(self):

        # Filter by entry properties, return a list of entries

        pass

    def get_download_urls(self, entry_id):

        # Resolve links from mirrors

        entry = next(item for item in self.entries if item['id'] == entry_id)
        try:
            soup = make_soup(entry['mirrors'][0])  # Mirror 1 by default
        except (URLError, HTTPError):
            print("ERROR - Connection error (Mirror 1).")
        else:
            urls = [lnk['href'] for lnk in soup.find_all('a', string=SOURCES)]

        return urls

    def download(self, entry_id, path):

        # Download by ID, default method is GET from the first mirror

        entry = next(item for item in self.entries if item['id'] == entry_id)
        print(f"DEBUG - {entry['id']}: {entry['title']}")  # debug
        filename = f"{entry['id']}.{entry['ext']}"
        urls = self.get_download_urls(entry_id)
        for url in urls:
            try:
                print("DEBUG - downloading...")  # debug
                print(f"  {url[:60]}")  # debug
                urlretrieve(url, f"{path}/{filename}")
            except (URLError, HTTPError):
                print("ERROR - Connection error (download).")
                continue
            else:
                print("DEBUG - done!")  # debug
                break
