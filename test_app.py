import json
import os
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import Actors, Movies, db, db_drop_and_create_all, setup_db
from auth_test_setup import get_token


assistant_token = get_token('assistant')
director_token = get_token('director')
producer_token = get_token('producer')

print(assistant_token)


class MoviesTest(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = app.test_client
        database_path = "postgres://{}@{}/{}".format(
            # os.getenv('DATABASE_USER'),
            # os.getenv('DATABASE_PORT'),
            # os.getenv('DATABASE_HOST'),
            # os.getenv("DATABASE_NAME")
            'postgresql', 'localhost:5432', "Udacity"
        )
        setup_db(app)

    def tearDown(self):
        db_drop_and_create_all()

    def test_add_movie(self):
        response = self.client().post(
            '/movies',
            content_type='application/json',
            data=json.dumps({"title": "nicks", "release_date": "2019/2/2"}),
            headers={'Authorization': f'Bearer {producer_token}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_add_movie_fail(self):
        response = self.client().post(
            '/movies',
            content_type='application/json',
            headers={'Authorization': f'Bearer {producer_token}'},
            data=json.dumps({"title": "", "release_date": ""})
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'incorrect movie title')

    def test_add_actor(self):
        response = self.client().post(
            '/actors',
            content_type='application/json',
            headers={'Authorization': f'Bearer {director_token}'},
            data=json.dumps({"name": "nicks", "age": "20", "gender": "male"})
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_add_actor_fail(self):
        response = self.client().post(
            '/actors',
            content_type='application/json',
            headers={'Authorization': f'Bearer {director_token}'},
            data=json.dumps({"name": "", "age": "", "gender": ""})
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'incorrect name or name exists')

    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            content_type='application/json',
            headers={'Authorization': f'Bearer {assistant_token}'},
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_movies(self):
        response = self.client().get(
            '/movies',
            content_type='application/json',
            headers={'Authorization': f'Bearer {assistant_token}'},
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_single_actor(self):
        self.client().post(
            '/actors',
            content_type='application/json',
            headers={'Authorization': f'Bearer {director_token}'},
            data=json.dumps({"name": "done", "age": "1", "gender": "male"})
        )
        response = self.client().get(
            '/actors/1',
            headers={'Authorization': f'Bearer {director_token}'},
            content_type='application/json'
        )
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 1)

    def test_get_single_actor_error(self):
        self.client().post(
            '/actors',
            content_type='application/json',
            headers={'Authorization': f'Bearer {director_token}'},
            data=json.dumps({"name": "done", "age": "1", "gender": "male"})
        )
        response = self.client().get(
            '/actors/10',
            headers={'Authorization': f'Bearer {director_token}'},
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 0)

    def test_edit_actor(self):
        self.client().post(
            '/actors',
            content_type='application/json',
            headers={'Authorization': f'Bearer {director_token}'},
            data=json.dumps({"name": "done", "age": "1", "gender": "male"})
        )
        response = self.client().patch(
            '/actors/1/edit',
            content_type='application/json',
            headers={'Authorization': f'Bearer {director_token}'},
            data=json.dumps({"name": "bradley"})
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_edit_actor_error(self):
        response = self.client().patch(
            '/actors/2/edit',
            content_type='application/json',
            headers={'Authorization': f'Bearer {director_token}'},
            data=json.dumps({"name": "bradley"})
        )
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'actor not found')

    def test_edit_movie(self):
        self.client().post(
            '/movies',
            content_type='application/json',
            headers={'Authorization': f'Bearer {producer_token}'},
            data=json.dumps({"title": "done", "release_date": "2020/2/2"})
        )
        response = self.client().patch(
            '/movies/1/edit',
            content_type='application/json',
            headers={'Authorization': f'Bearer {producer_token}'},
            data=json.dumps({"title": "bradley"})
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_edit_movie_error(self):
        response = self.client().patch(
            '/movies/2/edit',
            content_type='application/json',
            headers={'Authorization': f'Bearer {producer_token}'},
            data=json.dumps({"title": "bradley"})
        )
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'movie not found')

    def test_delete_movie(self):
        self.client().post(
            '/movies',
            content_type='application/json',
            headers={'Authorization': f'Bearer {producer_token}'},
            data=json.dumps({"title": "done", "release_date": "2020/2/2"})
        )
        response = self.client().delete(
            '/movie/1/delete',
            headers={'Authorization': f'Bearer {producer_token}'},
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], '1 deleted')

    def test_delete_actor(self):
        self.client().post(
            '/actors',
            content_type='application/json',
            headers={'Authorization': f'Bearer {director_token}'},
            data=json.dumps({"name": "done", "age": "20", "gender": "male"})
        )
        response = self.client().delete(
            '/actor/1/delete',
            headers={'Authorization': f'Bearer {director_token}'},
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], '1 deleted')

    def test_delete_movie_error(self):
        self.client().post(
            '/movies',
            content_type='application/json',
            headers={'Authorization': f'Bearer {producer_token}'},
            data=json.dumps({"title": "done", "release_date": "2020/2/2"})
        )
        response = self.client().delete(
            '/movie/10/delete',
            headers={'Authorization': f'Bearer {producer_token}'},
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'no results found')

    def test_delete_actor_error(self):
        self.client().post(
            '/actors',
            content_type='application/json',
            headers={'Authorization': f'Bearer {producer_token}'},
            data=json.dumps({"name": "done", "age": "20", "gender": "male"})
        )
        response = self.client().delete(
            '/actor/10/delete',
            headers={'Authorization': f'Bearer {producer_token}'},
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'no results found')


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = app
        self.client = self.app.test_client

    def test_get_actors_without_authorization_headers(self):

        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {
            'success': False,
            'error': 401,
            'message': 'invalid_header: Authorization header missing'
        })

    def test_get_actors_with_bearer_missing_from_auth_headers(self):

        response = self.client().get(
            '/actors',
            headers={'Authorization': 'hshdkdkkdkkkkdkddl'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {
            'success': False,
            'error': 401,
            'message': '''invalid_header: "Bearer" missing from Authorization header'''
        })

    def test_get_actors_with_token_missing_from_auth_headers(self):

        response = self.client().get(
            '/actors',
            headers={'Authorization': 'Bearer '})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data, {
            'success': False,
            'error': 401,
            'message': '''invalid_header: Token missing from Authorization header'''
        })

    def test_get_actors_with_invalid_auth_headers(self):
        invalid_header = {
            'Authorization': 'Bearer hddjsskks  token'}

        response = self.client().get(
            '/actors',
            headers=invalid_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

