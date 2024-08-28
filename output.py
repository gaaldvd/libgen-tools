import ast
from test import list_entries, parse_args
from libgen_tools import FILTERS


def filter_entries(filters, entries, mode):

    results = entries
    for key, value in zip(filters.keys(), filters.values()):
        if mode == "exact":
            results = [e for e in results
                       if value.lower() == e[FILTERS[key]].lower()]
        elif mode == "partial":
            results = [e for e in results
                       if value.lower() in e[FILTERS[key]].lower()]

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
        f_mode = "exact" if f_seq[0] == "-e" else "partial"
        f_seq = f_seq[1:]
        print(f_mode, f_seq)
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
        list_entries(filter_entries(filters, entries, f_mode))


if __name__ == '__main__':
    main()
