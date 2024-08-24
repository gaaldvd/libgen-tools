import sys
import argparse
from os.path import dirname, abspath
from libgen_tools import SearchRequest, QueryError


def parse_args():

    # Parsing CLI arguments

    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    return parser.parse_args()


def main():

    # Test script with CLI arguments

    args = parse_args()
    query = args.query
    try:
        request = SearchRequest(query=query)
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

    print("\nNo.".ljust(5) + "Author".ljust(24) + "Title".ljust(34)
          + "Year".ljust(5) + "Pages".ljust(9) + "Extension\n".ljust(10)
          + "-" * 85)
    for entry, i in zip(results.entries, range(len(results.entries))):
        auth = entry['auth']
        title = entry['title']
        year = entry['year']
        pp = entry['pp']
        ext = entry['ext']
        print(f"{i + 1:<4}"
              f" {auth[:20] + '...' if len(auth) > 20 else auth:<23}"
              f" {title[:30] + '...' if len(title) > 30 else title:<33}"
              f" {year:<4} {pp[:8]:<8} {ext:<9}")

    # Prompt for download

    num = input("Enter entry number to download [or press Return to exit]: ")
    if not num:
        sys.exit("Goodbye!")
    elif num in range(len(results.entries)):
        results.download(559585, dirname(abspath(sys.argv[0])))


if __name__ == '__main__':
    main()
