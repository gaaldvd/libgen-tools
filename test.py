import sys
import argparse
from os.path import dirname, abspath
from libgen_tools import SearchRequest, QueryError


def parse_args():

    # Parse CLI arguments

    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    return parser.parse_args()


def list_entries(entries):

    # List results

    print("\nNo.".ljust(5) + "Author".ljust(24) + "Title".ljust(34)
          + "Year".ljust(5) + "Pages".ljust(9) + "Extension\n".ljust(10)
          + "-" * 85)
    for entry, i in zip(entries, range(len(entries))):
        auth = entry['auth']
        title = entry['title']
        year = entry['year']
        pp = entry['pp']
        ext = entry['ext']
        print(f"{i + 1:<4}"
              f" {auth[:20] + '...' if len(auth) > 20 else auth:<23}"
              f" {title[:30] + '...' if len(title) > 30 else title:<33}"
              f" {year:<4} {pp[:8]:<8} {ext:<9}")


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

    if input("\nEnter 'y' to list entries (Return to skip) > ") in ("y", "Y"):
        list_entries(results.entries)

    # Filter results

    if input("\nEnter 'y' to filter entries"
             "(Return to skip) > ") in ("y", "Y"):
        pass

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
