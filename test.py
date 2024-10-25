"""Test script of libgen-tools."""

import sys
from os.path import dirname, abspath
from libgentools import SearchRequest, Results, QueryError, FilterError


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
    """Main function of the test script."""

    # Fetch results from the LibGen website
    try:
        request = SearchRequest("The Corfu Trilogy")
    except QueryError as qerr:
        results = None
        sys.exit(qerr)
    except ConnectionError as cerr:
        results = None
        sys.exit(cerr)
    else:
        print(f"\nQuery: {request.query}")
        results = Results(request.results)
        print(f"{len(results.entries)} entries found.")

    # Listing results
    list_entries(results.entries)

    # Filtering results
    try:
        filters = {'auth': "Gerald Durrell"}
        mode = "exact"
        if filters:
            print(f"\nFiltering mode: {mode}")
            print("Filters")
            for key, value in zip(filters.keys(), filters.values()):
                print(f"  {key + ':':<6} {value}")
            results = results.filter_entries(filters, mode)
            print(f"{len(results.entries)} entries found.")
            list_entries(results.entries)
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
                  f" 1 and {len(results.entries)}!")
            continue
        else:
            entry = results.entries[num - 1]
            print(f"  Downloading {entry['id']}: {entry['title']}...")
            results.download(entry, dirname(abspath(sys.argv[0])))
            print("  Done!")
            break


if __name__ == '__main__':
    main()
