"""Handle search requests and manage results."""

from urllib.request import urlopen, urlretrieve
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

# Possible download sources
SOURCES = ("GET", "Cloudflare", "IPFS.io", "Infura", "Pinata")

# Used in validation and filtering sequences
FILTERS = {'-a': "auth",
           '-t': "title",
           '-y': "year",
           '-l': "lang",
           '-e': "ext"}


def make_soup(url):
    """Make soup-making easier."""

    try:
        with urlopen(url) as page:
            html = page.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            return soup
    except (URLError, HTTPError) as cerr:
        raise ConnectionError("Connection error while making soup!") from cerr


class QueryError(Exception):
    """Raise when query is too short."""


class FilterError(Exception):
    """Raise when an invalid filter is encountered."""


class SearchRequest:
    """Handles search requests and generates a list of results.

    Attributes:
        query (str): The search query for the request.
            Could be an author, title or ISBN.
            Serves as a parameter for the constructor.

        results (list): A list of SEDs generated from the search query.
    """

    url_base = "https://www.libgen.is/search.php?column=def&req="

    def __init__(self, query=None):
        """Constructor method.

        :param str query: The search query for the request (default is None).

        :raises QueryError: If `query` is empty or less than 3 characters.
        """

        self.query = query
        if not self.query or len(self.query) < 3:
            raise QueryError("Search string must contain"
                             "at least 3 characters!")
        self.request_url = f"{self.url_base}{self.query.replace(" ", "+")}"
        self.raw_results = self.get_results(self.request_url)
        self.results = self.create_entry_list(self.raw_results)

    def get_results(self, url):
        """Scrape and return results from the LibGen website.

        :param str url: The Libgen URL of the request.
            Concatenated from the `url_base` and `query` variables.

        :return: A raw list of BeautifulSoup objects.
            The list contains the <tr> tags from every page of
            search results from the LibGen website.
        :rtype: list
        """

        table = []
        soup = make_soup(url)
        result_count = int(soup.find_all('table')[1].text.split()[0])
        page_count = result_count // 25

        # Merging raw results from every page into table
        pages = [soup.find_all('table')[2].find_all('tr')[1:]]
        if page_count > 1:
            for i in range(page_count):
                soup = make_soup(f"{self.request_url}&page={i + 2}")
                pages.append(soup.find_all('table')[2].find_all('tr')[1:])
        for page in pages:
            for row in page:
                table.append(row)

        # Returning the raw results as a list of BeautifulSoup objects
        return table

    def create_entry_list(self, table):
        """Create and return a list of entries as a list of SEDs.

        :param list table: A raw list of BeautifulSoup objects.
            Contains <tr> tags, returned by the `get_results` method.

        :return: A list of standard entry dictionaries.
        :rtype: list
        """

        entry_list = []

        # Generating a list of dictionaries from table
        for row in table:
            columns = row.find_all('td')

            # Extracting ISBN and removing <i> tags from the Title column:
            i_tags = [tag.text for tag in columns[2].find_all('i') if tag]
            isbn = (i_tags[len(i_tags) - 1].replace("-", "").split(", ")
                    if len(i_tags) > 0 else None)
            i_tags = [tag.decompose() for tag in columns[2].find_all('i')]
            del i_tags

            # Adding entry to the list of SEDs
            entry = {'id': int(columns[0].text),
                     'isbn': isbn,
                     'auth': columns[1].text,
                     'title': columns[2].text,
                     'pub': columns[3].text if columns[3].text else None,
                     'pp': (None if columns[5].text in ("0", "")
                            else columns[5].text),
                     'lang': columns[6].text if columns[6].text else None,
                     'size': columns[7].text,
                     'ext': columns[8].text}
            try:
                entry['year'] = int(columns[4].text)
            except ValueError:
                entry['year'] = None
            else:
                entry['year'] = None if entry['year'] == 0 else entry['year']
                mirrors = [c.find('a')['href'] for c in columns[9:]
                           if c.find('a').text != "[edit]"]
                entry['mirrors'] = mirrors
                entry_list.append(entry)

        # Returning the results as a list of SEDs
        return entry_list


class Results:
    """Stores and manages search results.

    Attributes:
        entries (list): Stores the results as a list of SEDs.

    Methods:
        filter_entries(filters, mode="partial"):
            Filters results by a standard filtering dictionary.
            Partial or exact filtering are both available modes.

        download(entry, path):
            Downloads the selected entry to a specified location.
    """

    def __init__(self, results):
        """Constructor method.

        :param list results: A list of SEDs, returned either by
            `SearchRequest.create_entry_list` or `Results.filter_entries`.
        """

        self.entries = results

    def filter_entries(self, filters, mode="partial"):
        """Filter by entry properties and return a new Results instance.

        :param dict filters: A standard filter dictionary.
        :param str mode: The filtering mode used by the method (exact/partial).

        :return: A new instance of the `Results` class. The constructor of
            the new instance uses the list of SEDs generated by this
            method as a parameter.
        :rtype: Results

        :raises FilterError: If an invalid filter is encountered.
        """

        results = self.entries

        # Validating filters
        for f in [*filters]:
            if f not in [*FILTERS.values()]:
                raise FilterError(f"Invalid filter: {f}")

        for key, value in zip(filters.keys(), filters.values()):

            # Filtering by year
            if key == "year":
                if len(value) == 4 and value.isnumeric():
                    results = [e for e in results if value == str(e[key])]
                elif (len(value) == 9
                      and value[4] == "-"
                      and value.replace("-", "").isnumeric()):
                    years = value.split("-")
                    results = [e for e in results
                               if years[0] <= str(e[key]) <= years[1]]
                else:
                    raise FilterError(f"Invalid year: {value}")
                continue

            # Filtering by any other property
            if mode == "exact":
                results = [e for e in results
                           if value.lower() == e[key].lower()]
            elif mode == "partial":
                results = [e for e in results
                           if value.lower() in e[key].lower()]

        return Results(results)

    def get_download_urls(self, entry):
        """Resolve links from mirror(s).

        :param dict entry: The entry (SED) selected for downloading.

        :return: A list of the download URLs as strings.
        :rtype: list
        """

        try:
            # Mirror 1 by default
            soup = make_soup(entry['mirrors'][0])
        except (URLError, HTTPError):
            print("Connection error while connecting to Mirror 1!")
        else:
            urls = [lnk['href'] for lnk in soup.find_all('a', string=SOURCES)]

        return urls

    def download(self, entry, path):
        """Download entry, default method is GET from the first mirror.

        :param dict entry: The entry (SED) selected for downloading.
        :param str path: The path of the folder where the file should be
            downloaded to.
        """

        filename = f"{entry['id']}.{entry['ext']}"
        urls = self.get_download_urls(entry)
        for url in urls:
            try:
                urlretrieve(url, f"{path}/{filename}")
            except (URLError, HTTPError):
                print("Connection error while downloading!")
                downloaded = False
                continue
            else:
                downloaded = True
                break

        return downloaded
