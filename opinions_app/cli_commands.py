import csv

import click

from . import app, db
from .models import Opinion


@app.cli.command('load_opinions')
def load_opinions_command():
    """Функция загрузки мнений из файла CSV в базу данных."""
    with open('opinions.csv', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        counter = 0
        for row in reader:
            opinion = Opinion(**row)
            db.session.add(opinion)
            db.session.commit()
            counter += 1
    click.echo(f'Загружено мнений {counter}')