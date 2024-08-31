import ast
from test import list_entries, get_args
from libgen_tools import FILTERS


def parse_filtering_seq():
    pass


def filter_entries(filters, entries, mode):

    results = entries
    for key, value in zip(filters.keys(), filters.values()):
        if mode == "exact":
            results = [e for e in results if value.lower() == e[key].lower()]
        elif mode == "partial":
            results = [e for e in results if value.lower() in e[key].lower()]

    return results


def main():

    entries = []
    with open("table", "r") as f:
        entries = [ast.literal_eval(x) for x in f]

    args = get_args()
    print(f"\nDEBUG - args: {args}")

    if args['filters']:
        filters = args['filters']
        print(f"DEBUG - filtering mode: {args['mode']}")
        print(f"DEBUG - filters: {args['filters']}")
        entries = filter_entries(filters, entries, args['mode'])
    else:
        filters = None

    if input("\nEnter 'y' to list entries (Return to skip) > ") in ("y", "Y"):
        list_entries(entries)

    if input("\nEnter 'y' to filter entries (Return to skip) > ") in ("y", "Y"):
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
