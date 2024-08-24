import ast

entries = []

with open("table", "r") as f:
    for x in f:
        entries.append(ast.literal_eval(x))

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
