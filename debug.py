import sys
import ast
from test import list_entries, get_args
from libgen_tools import FILTERS, FilterError


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
                    raise FilterError(f"Invalid filter option: {segment}")
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

    for f in [*filters]:
        if f not in [*FILTERS.values()]:
            raise FilterError(f"Invalid filter: {f}")

    results = entries
    for key, value in zip(filters.keys(), filters.values()):
        if key == "year":
            if len(value) == 4 and value.isnumeric():
                results = [e for e in results if value == str(e[key])]
            elif (len(value) == 9
                  and value[4] == "-"
                  and value.replace("-", "").isnumeric()):
                years = value.split("-")
                results = [e for e in results
                           if years[0] <= str(e[key]) <= years[1]]
            else:
                raise FilterError(f"Invalid year: {value}")
            continue
        if mode == "exact":
            results = [e for e in results if value.lower() == e[key].lower()]
        elif mode == "partial":
            results = [e for e in results if value.lower() in e[key].lower()]

    return results


def main():

    with open("table", "r") as f:
        entries = [ast.literal_eval(x) for x in f]

    args = get_args()
    print(f"\nDEBUG - args: {args}")

    if args['filters']:
        filters = args['filters']
        print(f"DEBUG - filtering mode: {args['mode']}")
        print(f"DEBUG - filters: {args['filters']}")
        try:
            entries = filter_entries(filters, entries, args['mode'])
        except FilterError as ferr:
            sys.exit(ferr)
    else:
        filters = None

    if input("\nEnter 'y' to list entries (Return to skip) > ") in ("y", "Y"):
        list_entries(entries)

    if (input("\nEnter 'y' to filter entries (Return to skip) > ")
       in ("y", "Y")):
        sequence = input("\nFiltering sequence: ").split()
        mode = "exact" if "-x" in sequence else "partial"
        sequence = [f for f in sequence if f != "-x"]
        try:
            filters = parse_filtering_seq(sequence)
            if filters:
                entries = filter_entries(filters, entries, mode)
                list_entries(entries)
        except IndexError:
            print("Invalid filtering sequence!")
            filters = None
        except FilterError as ferr:
            sys.exit(ferr)


if __name__ == '__main__':
    main()
