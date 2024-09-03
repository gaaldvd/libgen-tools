# getting urls from mirror2 (http error 403)
try:
    soup = make_soup(entry['mirrors'][1])
except (URLError, HTTPError):
    print("ERROR - Connection error (Mirror 2).")
    print(f"DEBUG - mirror2 url: {entry['mirrors'][1]}")  # debug
else:
    urls.append(soup.find_all('a', string="<h2>GET</h2>"))


# writing entries into a file
with open("table", "w") as f:
    for entry in results.entries:
        f.write(str(entry) + "\n")

