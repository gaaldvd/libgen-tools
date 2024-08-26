import ast
import argparse

FILTERS = {'-a': "auth",
           '-t': "title",
           '-y': "year",
           '-l': "lang",
           '-e': "ext"}


def parse_args():

    # Parsing CLI arguments

    parser = argparse.ArgumentParser()
    parser.add_argument("")
    return parser.parse_args()


def list_entries(entries):
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


def filter_entries(filters, entries):
    print("\nfilters:")
    for key, value in zip(filters.keys(), filters.values()):
        print(f"  {FILTERS[key]}: {value}")
    results = entries
    for key, value in zip(filters.keys(), filters.values()):
        results = [e for e in results if e[FILTERS[key]].lower() == value]
    print(f"filtered results: {len(results)}")
    return results


def main():
    # args = parse_args()
    entries = []
    with open("table", "r") as f:
        for x in f:
            entries.append(ast.literal_eval(x))

    if input("Enter 'y' to list entries (Return to skip) > ") in ("y", "Y"):
        list_entries(entries)

    if input("Enter 'y' to filter entries (Return to skip) > ") in ("y", "Y"):
        f_seq = input("Filtering sequence > ").split()
        print(f_seq)
        filters = {}
        for f in f_seq:
            if f[0] == "-":
                filters[f] = ""
                fil = f
            else:
                filters[fil] += f" {f}"
                if len(filters[fil].split()) == 1:
                    filters[fil] = filters[fil].strip()
        print(filters)
        list_entries(filter_entries(filters, entries))


if __name__ == '__main__':
    main()
