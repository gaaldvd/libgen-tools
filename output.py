import ast

FILTERS = {'-a': "auth",
           '-t': "title",
           '-y': "year",
           '-l': "lang",
           '-e': "ext"}


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
    filtered_results = entries
    for key, value in zip(filters.keys(), filters.values()):
        filtered_results = [entry for entry in filtered_results if entry[FILTERS[key]] == value]
    print(f"filtered results: {len(filtered_results)}")
    return filtered_results


def main():
    entries = []
    with open("table", "r") as f:
        for x in f:
            entries.append(ast.literal_eval(x))

    if input("list entries? ") in ("y", "Y"):
        list_entries(entries)

    filters = {'-a': "Jane Austen", '-e': "pdf"}
    # filtered_results = filter_entries(filters, entries)
    list_entries(filter_entries(filters, entries))


if __name__ == '__main__':
    main()
