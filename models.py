import os
import json
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy


# database_filename = "database.db"
# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = "sqlite:///{}".format(
#     os.path.join(project_dir, database_filename))
database_path = "postgres://{}@{}/{}".format(
  'postgres', 'localhost:5432', "Udacity"
  )

db = SQLAlchemy()

# db setup


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

# refresh database
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Movies(db.Model):

    __tablename__ = 'movies'

    id = Column(Integer().with_variant(
        Integer, "sqlite"), primary_key=True)
    title = Column(String, nullable=False, unique=True)
    release_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        self.updated_at = datetime.now()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "title": self.title,
            "release_date": self.release_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at

        }


class Actors(db.Model):

    __tablename__ = 'actors'

    id = Column(Integer().with_variant(
        Integer, "sqlite"), primary_key=True)
    name = Column(String, nullable=False, unique=True)
    age = Column(Integer(), nullable=False)
    gender = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        self.updated_at = datetime.now()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
