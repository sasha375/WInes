from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
from math import floor

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
from pprint import pprint
from collections import defaultdict

wines = pandas.read_excel('wine.xlsx', sheet_name='Лист1', na_values='', keep_default_na=False).fillna('').to_dict(orient='record')
final_wines = defaultdict(list)
for wine in wines:
    wine_without_cat = wine.copy()
    del wine_without_cat["Категория"]

    final_wines[wine["Категория"]].append(wine_without_cat)

final_wines = dict(final_wines)

categories = []
for cat, wines in final_wines.items():
    categories.append({"name":cat, "wines":wines})


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