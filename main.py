import datetime
from math import floor
import pandas

from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

wines = pandas.read_excel('wine.xlsx', sheet_name='Лист1', na_values='', keep_default_na=False).fillna('').to_dict(orient='record')
drinks = defaultdict(list)
for wine in wines:
    wine_without_cat = wine.copy()
    del wine_without_cat["Категория"]

    drinks[wine["Категория"]].append(wine_without_cat)

drinks = dict(drinks)

categories = []
for cat, wines in drinks.items():
    categories.append({"name": cat, "wines": wines})


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


rendered_page = template.render(
    lifetime=floor((datetime.datetime.now().date() - datetime.date(1920, 1, 1)).total_seconds() / (3600 * 24 * 360)),
    categories=categories
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
