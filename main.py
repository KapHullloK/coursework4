from flask import Flask
from flask_cors import CORS

from flask_restx import Api

from create_db import create_data

from views.movie import movies_ns
from views.director import directors_ns
from views.genre import genres_ns
from views.user import auth_ns, user_ns

from config import Config
from setup_db import db

api = Api(doc="/docs")


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    register(app)
    return app


def register(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movies_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    create_data(app, db)


app = create_app(Config())
CORS(app)

app.url_map.strict_slashes = False

if __name__ == '__main__':
    app.debug = True
    app.run()
