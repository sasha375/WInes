from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
from math import floor
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
from pprint import pprint
from collections import defaultdict

wines = pandas.read_excel('wine3.xlsx', sheet_name='Лист1', na_values='', keep_default_na=False).fillna('').to_dict(orient='record')
d = defaultdict(list)
for v in wines:
    v2 = v.copy()
    del v2["Категория"]

    d[v["Категория"]].append(v2)

d = dict(d)
categories = []
for k, v in d.items():
    categories.append({"name":k, "wines":v})



pprint(d)

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