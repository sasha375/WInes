import collections
import datetime
import sys
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

import argparse
import pandas

from jinja2 import Environment, FileSystemLoader, select_autoescape


def main():
    parser = argparse.ArgumentParser(description='Описание что делает программа')
    parser.add_argument('--production-path', default=os.getenv("PRODUCTION_PATH"), help="path to xlsx file (If param is not specified it will be given from Environment)")
    parser.add_argument('--sheet-name', default=os.getenv("SHEET_NAME"), help="sheet name in <--production-path> (If param is not specified it will be given from Environment)")
    args = parser.parse_args()
    
    wines = pandas.read_excel(args.production_path, sheet_name=args.sheet_name, na_values='', keep_default_na=False).fillna('').to_dict(orient='record')
    
    creation_year = 1920
    
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
        lifetime=datetime.datetime.now().year - creation_year,
        production=production
    )
        with open('index.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()