from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from collections import defaultdict
import pandas


def get_year_form(num):
    if 11 <= num % 100 <= 20:
        return "лет"
    else:
        if num % 10 == 1:
            return "год"
        elif 2 <= num % 10 <= 4:
            return "года"
        else:
            return "лет"


def get_link_to_excel():
    parser = argparse.ArgumentParser(description='Сайт Новое русское вино')
    parser.add_argument('-l', '--link_to_excel', default='wine3.xlsx', help='Ссылка на ваш excel файл')
    args = parser.parse_args()
    return args.link_to_excel


def main():
    link = get_link_to_excel()
    wine_characteristics = pandas.read_excel(io=link, na_values=['N/A', 'NA'], keep_default_na=False))
    wine_characteristics = wine_characteristics.fillna("")

    grouped_characteristics = defaultdict(list)
    for _, row in wine_characteristics.iterrows():
        grouped_characteristics[row["Категория"]].append(row.to_dict())


    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    current_year = datetime.now().year
    winery_age = current_year - 1920
    year_form = get_year_form(winery_age)

    template = env.get_template('template.html')

    rendered_page = template.render(
        winery_age=f"{winery_age} {year_form}",
        grouped_characteristics=grouped_characteristics
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
