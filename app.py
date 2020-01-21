import os
import json
from datetime import datetime
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Actors, Movies, db, db_drop_and_create_all, setup_db, database_path


# def create_app(test_config=None):
# create and configure the app
app = Flask(__name__)
CORS(app)
setup_db(app)

# return app
# db_drop_and_create_all()


@app.route('/')
def home():
    return ('I am cool')


@app.route('/movies', methods=['POST'])
def add_movie():
    movie = Movies.query.all()
    keys = ("release_date", "title")
    data = request.get_json()
    # if data not in keys:
    #     return jsonify({
    #         'success': 'false',
    #         'message': 'fill in the missing fields'
    #     }), 400
    # if not data['release_date'] == '' or not data['release_date']:
    #     return jsonify({
    #         'success': 'false',
    #         'message': 'please add the release_date'
    #     }), 400

    if 15 < len(data['title']) < 3 or not data['title'].isalnum() or \
            bool(Movies.query.filter_by(title=data['title']).first()):
        return jsonify({
            'success': 'false',
            'message': 'incorrect movie title'
        }), 400
    else:
        final_data = Movies(title=data['title'],
                            release_date=data['release_date'])
        db.session.add(final_data)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '{} movie created successfully'.format(data['title'])
        }), 200


@app.route('/movies')
def retrieve_movies():
    data = Movies.query.all()
    return jsonify({
        'data': [movie.format() for movie in data],
        'success': True
    }), 200

@app.route('/movies/<int:id>')
# @jwt_required
def get_a_single_movie(id):
    try:
        data=Movies.query.filter_by(id=id)
        if not data:
            return jsonify({
                'success': 'false',
                'message': 'no results found'
        }), 404
        else:
            return jsonify(
                {
                    'success': True,
                    'data': [i.format() for i in data],
                }
            ),200
    except Exception as error:
        return error

@app.route('/actors/<int:id>')
# @jwt_required
def get_a_single_actor(id):
    try:
        data=Actors.query.filter_by(id=id)
        if not data:
            return jsonify({
                'success': 'false',
                'message': 'no results found'
        }), 404
        else:
            return jsonify(
                {
                    'success': True,
                    'data': [i.format() for i in data],
                }
            ),200
    except Exception as error:
        return error

@app.route('/actors')
def retrieve_actors():
    data = Actors.query.all()
    return jsonify({
        'data': [actor.format() for actor in data],
        'success': True
    }), 200


@app.route('/actors', methods=['POST'])
def add_actors():
    movie = Actors.query.all()
    keys = ["name", "age", "gender"]
    gender_list = ["male", "female"]
    data = request.get_json()
    # if data not in keys:
    #     return jsonify({
    #         'success': 'false',
    #         'message': 'fill in the missing fields'
    #     }), 400

    if 15 < len(data['name']) < 3 or not data['name'].isalnum() or \
            bool(Actors.query.filter_by(name=data['name']).first()):
        return jsonify({
            'success': 'false',
            'message': 'incorrect name or name exists'
        }), 400

    elif len(data['age']) > 2 and not isinstance((data['age']), int):
        return jsonify({
            'success': 'false',
            'message': 'invalid age'
        }), 400
    elif (data['gender']) not in gender_list and not isinstance((data['gender']), str):
        return jsonify({
            'success': 'false',
            'message': 'invalid gender'
        }), 400
    else:
        final_data = Actors(name=data['name'],
                            age=data['age'], gender=data['gender'])
        db.session.add(final_data)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '{}  created successfully'.format(data['name'])
        }), 200


@app.route('/movies/<id>/edit', methods=['PATCH'])
# @requires_auth('patch:drinks')
def edit_movie_details(id):
    movie = Movies.query.filter(Movies.id == id).one_or_none()
    if not movie:
        return jsonify({
            'success': 'false',
            'message': 'movie not found'
        }), 404
    for item in json.loads(request.data).keys():
        if item == 'title':
            title = json.loads(request.data)['title']
            movie.title = title
            Movies.updated_at = datetime.now()
            db.session.commit()
            return jsonify({
                'success': True,
                'movies': [movie.format()],
                "message": "updated"
            }), 200


@app.route('/actors/<id>/edit', methods=['PATCH'])
# @requires_auth('patch:drinks')
def edit_actors_details(id):
    actor = Actors.query.filter(Actors.id == id).one_or_none()
    if not actor:
        return jsonify({
            'success': 'false',
            'message': 'actor not found'
        }), 404
    for item in json.loads(request.data).keys():
        if item == 'name':
            name = json.loads(request.data)['name']
            actor.name = name
        if item == 'age':
            age = json.loads(request.data)['age']
            actor.age = age
        if item == 'gender':
            gender = json.loads(request.data)['gender']
            actor.gender = gender

        Actors.updated_at = datetime.now()
        db.session.commit()
        return jsonify({
            'success': True,
            'movies': [actor.format()],
            "message": "updated"
        }), 200

@app.route('/movie/<int:id>/delete', methods=['DELETE'])
# @jwt_required
def delete_a_single_movie(id):
    try:
        data=Movies.query.filter_by(id=id).one_or_none()
        if not data:
            return jsonify({
                'success': 'false',
                'message': 'no results found'
                }), 404

        data.delete()
        return jsonify(
            {
                'success': True,
                'message': '{} deleted'.format(id),
            }
        ), 200
    except Exception as error:
        return error


@app.route('/actor/<int:id>/delete', methods=['DELETE'])
# @jwt_required
def delete_a_single_actor(id):
    try:
        data=Actors.query.filter_by(id=id).one_or_none()
        if not data:
            return jsonify({
                'success': 'false',
                'message': 'no results found'
                }), 404

        data.delete()
        return jsonify(
            {
                'success': True,
                'message': '{} deleted'.format(id),
            }
        ), 200
    except Exception as error:
        return error

if __name__ == '__main__':
    app.run(debug=True)
