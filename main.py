import collections
import datetime
import pandas
import sys
import argparse
import os

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

error = False
__doc__ = '''
Usage:
  python main.py [--production-path PRODUCTION_PATH] [--sheet-name SHEET_NAME]
(If param is not specified it will be given from Environment)
'''

parser = argparse.ArgumentParser(description='Описание что делает программа')
parser.add_argument('--production-path', default=os.getenv("PRODUCTION_PATH"))
parser.add_argument('--sheet-name', default=os.getenv("SHEET_NAME"))
args = parser.parse_args()

if args.production_path is None:
    print("Error: production path does not specified")
    error = True

if args.sheet_name is None:
    print("Error: sheet name does not specified")
    error = True

if args.production_path is not None:
    if not os.path.exists(args.production_path):
        print("FileNotFoundError: file " + args.production_path + " does not exists")
        error = True

if error:
    print(__doc__)
    exit(1)

wines = pandas.read_excel(args.production_path, sheet_name=args.sheet_name, na_values='', keep_default_na=False).fillna('').to_dict(orient='record')

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
