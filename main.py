import collections
import datetime
from math import floor
import pandas

from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

wines = pandas.read_excel('wine.xlsx', sheet_name='Лист1', na_values='', keep_default_na=False).fillna('').to_dict(orient='record')

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
