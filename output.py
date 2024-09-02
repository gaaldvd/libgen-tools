import ast
from test import list_entries, get_args
from libgen_tools import FILTERS


def parse_filtering_seq(sequence):

    filters = {}
    if sequence[0] in [*FILTERS]:
        for segment in sequence:
            if segment[0] == "-":
                if segment in [*FILTERS]:
                    print(f"DEBUG - filter: {segment}")
                    key = FILTERS[segment]
                    filters[key] = ""
                else:
                    print(f"Invalid filter: {segment}")
                    filters = None
                    break
            else:
                filters[key] += f" {segment}"
                if len(filters[key].split()) == 1:
                    filters[key] = filters[key].strip()
        print(f"DEBUG - filters: {filters}")
    else:
        print("Invalid filtering sequence!")
        filters = None

    return filters


def filter_entries(filters, entries, mode):

    results = entries
    for key, value in zip(filters.keys(), filters.values()):
        if mode == "exact":
            results = [e for e in results if value.lower() == e[key].lower()]
        elif mode == "partial":
            results = [e for e in results if value.lower() in e[key].lower()]

    # TODO implement filtering by year

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

    if (input("\nEnter 'y' to filter entries (Return to skip) > ")
       in ("y", "Y")):
        sequence = input("\nFiltering sequence: ").split()
        mode = "exact" if "-x" in sequence else "partial"
        sequence = [f for f in sequence if f != "-x"]
        print(f"DEBUG - filtering sequence: {sequence}")
        print(f"DEBUG - filtering mode: {mode}")
        try:
            filters = parse_filtering_seq(sequence)
        except IndexError:
            print("Invalid filtering sequence!")
            filters = None
        if filters:
            entries = filter_entries(filters, entries, mode)
            list_entries(entries)


if __name__ == '__main__':
    main()
