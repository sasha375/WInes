import collections
import datetime
import pandas
import sys
import os

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

p = False
s = False

if len(sys.argv) >= 2:
    if sys.argv[1] != "!inherit":
        path = sys.argv[1]
        p = True
    if len(sys.argv) >= 3:
        if sys.argv[2] != "!inherit":
            sheet_name = sys.argv[2]
            s = True

if (not p) or (not s):
    if os.path.exists("config.py"):
        import config
        if not p:
            path = config.production_path
        if not s:
            sheet_name = config.sheet_name
    else:
        raise FileNotFoundError("""
please specify production path or write it to config.py
Usage:
    python main.py [path_to_production [sheet_name]]
config.py syntax:
    production_path = "path/to/production.xlsx"
    sheet_name = "Sheetname"
""")



wines = pandas.read_excel(path, sheet_name=sheet_name, na_values='', keep_default_na=False).fillna('').to_dict(orient='record')

run_year = 1920

grouped_drinks = collections.defaultdict(list)

for drink in wines:
    grouped_drinks[drink['Категория']].append(drink)

production = []
for cat, wines in grouped_drinks.items():
    production.append({"name": cat, "wines": wines})


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


rendered_page = template.render(
    lifetime=round(datetime.datetime.now().year - run_year),
    categories=production
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
