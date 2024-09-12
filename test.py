import sys
import argparse
from os.path import dirname, abspath
from libgentools import SearchRequest, QueryError, FILTERS, FilterError


def get_args():
    """Interpret CLI arguments and return them as a dictionary."""
    parser = argparse.ArgumentParser(
        prog="test",
        description="Test script for libgen-tools",
        argument_default=argparse.SUPPRESS,)

    parser.add_argument("query", help="search query: title, author or ISBN",
                        nargs="*", default=None)
    parser.add_argument("-x", "--exact", action="store_true", default=False,
                        help="look for exact matches when filtering")

    filters = parser.add_argument_group("filters")
    filters.add_argument("-a", "--auth", help="author",
                         nargs="+", metavar="\b")
    filters.add_argument("-t", "--title", help="title",
                         nargs="+", metavar="\b")
    filters.add_argument("-y", "--year", help="year, two possible formats:"
                         " [from]-[to] or [year]", metavar="\b")
    filters.add_argument("-l", "--lang", help="language, use the ISO 639"
                         " standard: English, Russian, etc.", metavar="\b")
    filters.add_argument("-e", "--ext", help="extension, use any of the common"
                         " extensions: pdf, epub, mobi, etc.", metavar="\b")

    args = {'query': (" ".join(parser.parse_args().query)
                      if parser.parse_args().query else None),
            'mode': "exact" if parser.parse_args().exact else "partial"}

    filters = vars(parser.parse_args())
    if 'auth' in filters:
        filters['auth'] = " ".join(filters['auth'])
    if 'title' in filters:
        filters['title'] = " ".join(filters['title'])
    del filters['query'], filters['exact']
    args['filters'] = filters if filters else None

    return args


def parse_filtering_seq(sequence):
    """Interpret filtering sequence and return a standard filter dictionary."""
    filters = {}
    if sequence[0] in [*FILTERS]:
        for segment in sequence:
            if segment[0] == "-":
                if segment in [*FILTERS]:
                    key = FILTERS[segment]
                    filters[key] = ""
                else:
                    raise FilterError(f"Invalid filter option: {segment}")
            else:
                filters[key] += f" {segment}"
                if len(filters[key].split()) == 1:
                    filters[key] = filters[key].strip()
    else:
        filters = None
        raise FilterError("Invalid filtering sequence!")

    return filters


def list_entries(entries):
    """Print entries from a list of standard entry dictionaries."""
    print("\nNo.".ljust(6) + "Author".ljust(24) + "Title".ljust(34)
          + "Year".ljust(5) + "Pages".ljust(9) + "Extension".ljust(10)
          + "ID".ljust(11) + "\n" + "-" * 96)
    for entry, i in zip(entries, range(len(entries))):
        auth = entry['auth']
        title = entry['title']
        year = "" if entry['year'] is None else str(entry['year'])
        pp = "" if entry['pp'] is None else entry['pp']
        ext = entry['ext']
        eid = str(entry['id'])
        print(f"{i + 1:<4}"
              f" {auth[:20] + '...' if len(auth) > 20 else auth:<23}"
              f" {title[:30] + '...' if len(title) > 30 else title:<33}"
              f" {year:<4} {pp[:8]:<8} {ext:<9} {eid:<10}")


def main():
    """Test script of libgen-tools with CLI arguments."""
    args = get_args()

    # Fetch results from the LibGen website
    try:
        request = SearchRequest(query=args['query'] if args['query']
                                else input("\nEnter search query: "))
    except QueryError as qerr:
        results = None
        sys.exit(qerr)
    except ConnectionError as cerr:
        results = None
        sys.exit(cerr)
    else:
        print(f"\nQuery: {request.query}")
        filters = args['filters']
        if filters:
            print(f"Filtering mode: {args['mode']}")
            print("Filters")
            for key, value in zip(filters.keys(), filters.values()):
                print(f"  {key + ':':<6} {value}")
            try:
                results = request.results.filter_entries(filters, args['mode'])
            except FilterError as ferr:
                sys.exit(ferr)
        else:
            results = request.results
        print(f"{len(results.entries)} entries found.")

    # Listing results
    if input("\nEnter 'y' to list entries (Return to skip) > ") in ("y", "Y"):
        list_entries(results.entries)

    # Filtering results with sequence
    if input("\nEnter 'y' to filter entries"
             " (Return to skip) > ") in ("y", "Y"):
        sequence = input("\nFiltering sequence: ").split()
        mode = "exact" if "-x" in sequence else "partial"
        sequence = [f for f in sequence if f != "-x"]
        try:
            filters = parse_filtering_seq(sequence)
            if filters:
                print(f"Filtering mode: {args['mode']}")
                print("Filters")
                for key, value in zip(filters.keys(), filters.values()):
                    print(f"  {key + ':':<6} {value}")
                results = results.filter_entries(filters, mode)
                list_entries(results.entries)
        except IndexError:
            print("Invalid filtering sequence!")
            filters = None
        except FilterError as ferr:
            sys.exit(ferr)

    # Downloading entry
    while True:
        num = input("\nEnter entry number to download (Return to skip) > ")
        if num == "":
            break
        try:
            num = int(num)
            if num < 1 or num > len(results.entries):
                raise ValueError
        except ValueError:
            print("\nEntry number must be between"
                  f"1 and {len(results.entries)}!")
            continue
        else:
            entry = results.entries[num - 1]
            print(f"  Downloading {entry['id']}: {entry['title']}...")
            results.download(entry, dirname(abspath(sys.argv[0])))
            print("  Done!")
            break


if __name__ == '__main__':
    main()
