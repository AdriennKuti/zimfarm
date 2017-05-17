from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from flask_oauthlib.provider import OAuth2Provider


flask = Flask(__name__)
flask.config.update({
    'SQLALCHEMY_DATABASE_URI': 'sqlite:////zimfarm.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
})
db = SQLAlchemy(flask)
celery = Celery('worker', broker='amqp://admin:mypass@rabbit:5672', backend='redis://redis:6379/0')
oauth = OAuth2Provider(flask)
# celery = Celery()


from JSONEncoder import ZimfarmDispatcherJSONEncoder
flask.json_encoder = ZimfarmDispatcherJSONEncoder