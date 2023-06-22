from flask import render_template, jsonify

from . import app, db


@app.errorhandler(500)
def internal_error(error):
    """
    Функция для отображения кастомный страницы
    с ошибкой 500
    :param error:
    :return:
    """
    # В таких случаях можно откатить незафиксированные изменения в БД
    db.session.rollback()
    return render_template('500.html'), 500


@app.cli.command('load_opinions')
def load_opinions_command():
    """Функция загрузки мнений в базу данных."""
    with open('opinions.csv', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        counter = 0
        for row in reader:
            opinion = Opinion(**row)
            db.session.add(opinion)
            db.session.commit()
            counter += 1
    click.echo(f'Загружено мнений {counter}')


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """
    Функция обработчик кастомного исключения для API.
    :param error:
    :return:
    """
    return jsonify(error.to_dict()), error.status_code
