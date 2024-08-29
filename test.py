import sys
import argparse
from os.path import dirname, abspath
from libgen_tools import SearchRequest, QueryError, FILTERS


def get_args():

    # Get CLI arguments

    parser = argparse.ArgumentParser(
        prog="test",
        description="Test script for libgen-tools",
        argument_default=argparse.SUPPRESS,
    )
    parser.add_argument("query", nargs="?", default=None)
    filters = parser.add_argument_group("filters")
    filters.add_argument("-a", "--auth")
    filters.add_argument("-t", "--title")
    filters.add_argument("-y", "--year")
    filters.add_argument("-l", "--lang")
    filters.add_argument("-e", "--ext")
    filters.add_argument("-m", "--mode", default="partial")

    args = {'query': parser.parse_args().query,
            'mode': parser.parse_args().mode}
    filters = vars(parser.parse_args())
    del filters['query']
    del filters['mode']
    args['filters'] = filters

    return args


def list_entries(entries):

    # List results

    print("\nNo.".ljust(6) + "Author".ljust(24) + "Title".ljust(34)
          + "Year".ljust(5) + "Pages".ljust(9) + "Extension".ljust(10)
          + "ID".ljust(11) + "\n" + "-" * 96)
    for entry, i in zip(entries, range(len(entries))):
        auth = entry['auth']
        title = entry['title']
        year = entry['year']
        pp = entry['pp']
        ext = entry['ext']
        eid = entry['id']
        print(f"{i + 1:<4}"
              f" {auth[:20] + '...' if len(auth) > 20 else auth:<23}"
              f" {title[:30] + '...' if len(title) > 30 else title:<33}"
              f" {year:<4} {pp[:8]:<8} {ext:<9} {eid:<10}")


def main():

    # Test script with CLI arguments

    args = get_args()
    print(f"DEBUG - args: {args}")
    try:
        request = SearchRequest(query=args['query'])
    except QueryError as qerr:
        results = None
        sys.exit(qerr)
    except ConnectionError as cerr:
        results = None
        sys.exit(cerr)
    else:
        print(f"\nQuery: {request.query}")
        results = request.results
        print(f"{len(results.entries)} entries found.")

    # List results

    if input("\nEnter 'y' to list entries (Return to skip) > ") in ("y", "Y"):
        list_entries(results.entries)

    # Filter results

    if input("\nEnter 'y' to filter entries"
             " (Return to skip) > ") in ("y", "Y"):
        filters = {'auth': "Jane Austen", 'ext': "pdf"}
        print("Filters:")
        for key, value in zip(filters.keys(), filters.values()):
            print(f"  {key}: {value}")
        results = results.filter_entries(filters, "partial")
        print(f"Filtered results: {len(results.entries)}")
        list_entries(results.entries)

    # Download entry

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
