from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .constants import NO_OPINION_IN_DB
from .forms import OpinionForm
from .models import Opinion


def random_opinion():
    """
    Функция для получения случайного объекта opinion
    модели Opinion.
    :return:
    """
    quantity = Opinion.query.count()
    if quantity:
        offset_value = randrange(quantity)
        opinion = Opinion.query.offset(offset_value).first()
        return opinion


@app.route('/')
def index_view():
    """
    Функция для рендеринга главной страницы http://127.0.0.1:5000/
    где рандомно отображается название и мнения о фильме.
    :return: str
    """
    opinion = random_opinion()
    if opinion is not None:
        return render_template('opinion.html', opinion=opinion)
    abort(404)


@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    """
    Функция для отображения форм из класса OpinionForm
    и валидации данных в формах с последующей записью данных
    в таблицу Opinion и перенаправлением
    на страницу http://127.0.0.1:5000/opinions/<int:id>.
    :return:
    """
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        if Opinion.query.filter_by(text=text).first() is not None:
            flash('Такое мнение уже было оставлено ранее!', category='free-message')
            return render_template('add_opinion.html', form=form)
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)


@app.route('/opinions/<int:id>')
def opinion_view(id: int) -> str:
    """
    Функция для формирования динамических URL адресов
    с помощью конвектора пути '<int:id>' и для отображения
    сформированной ссылки на странице http://127.0.0.1:5000/
    блок HTML шаблона, где указывается сформированная ссылка:
        'templates/opinion.html'
        '<p>
            Ссылка для друзей:
            <a href="{{ url_for('opinion_view', id=opinion.id) }}">
            {{ url_for('opinion_view', id=opinion.id) }}
            </a>
        </p>'.
    :param id: int
    :return: str
    """
    opinion = Opinion.query.get_or_404(id)
    return render_template('opinion.html', opinion=opinion)
