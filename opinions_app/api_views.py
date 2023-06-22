from flask import jsonify, request
from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import Opinion
from .views import random_opinion


@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id: int):
    """
    API-view функция для GET http-запроса на эндпоинт
    http://127.0.0.1:5000/api/opinions/<int:id>/
    и получения объекта(по id объекта) модели Opinion.
    :param id:
    :return: json object
    """
    opinion = Opinion.query.get_or_404(id)
    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    return jsonify({"opinion": opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id: int):
    """
    API-view функция для PATCH http-запроса на эндпоинт
    http://127.0.0.1:5000/api/opinions/<int:id>/
    и изменения любого атрибута объекта opinion.
    :param id:
    :return:
    """
    data = request.get_json()
    if (
        'text' in data and
        Opinion.query.filter_by(text=data['text']).first()
    ):
        raise InvalidAPIUsage('Такое мнение уже есть в базе данных')

    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)

    opinion = Opinion.query.get_or_404(id)
    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinion(id: int):
    """
    API-view функция для DELETE http-запроса на эндпоинт
    http://127.0.0.1:5000/api/opinions/<int:id>/
    и удаления объекта из БД.
    :param id:
    :return:
    """
    opinion = Opinion.query.get_or_404(id)
    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    db.session.delete(opinion)
    db.session.commit()
    return '', 204


@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    """
    API-view функция для GET http-запроса на эндпоинт
    http://127.0.0.1:5000/api/opinions/
    и получения всех объектов модели Opinion.
    :return:
    """
    opinions = Opinion.query.all()
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return jsonify({'opinions': opinions_list}), 200


@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    """
    API-view функция для POST http-запроса на эндпоинт
    http://127.0.0.1:5000/api/opinions/
    и добавление нового объекта opinion в БД.
    :return:
    """
    data = request.get_json()
    if 'title' not in data or 'text' not in data:
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')
    if Opinion.query.filter_by(text=data['text']).first():
        raise InvalidAPIUsage('Такое мнение уже есть в базе данных')
    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/get-random-opinion/', methods=['GET'])
def get_random_opinion():
    """
    API-view функция для GET http-запроса на эндпоинт
    http://127.0.0.1:5000/api/get-random-opinion/
    и получение случайного объекта opinion, модели Opinion.
    :return:
    """
    opinion = random_opinion()
    if opinion is not None:
        return jsonify({'opinion': opinion.to_dict()}), 200
    raise InvalidAPIUsage('В базе данных нет мнений', 404)
