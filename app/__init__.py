# -*- coding: utf-8 -*-
from flask import Flask
from lib.logger import get_logger
from configer import Config, gitlab_application, gitlab_secret, gitlab_base_url, gitlab_access_token_url, gitlab_authorize_url, \
    redis_host, redis_port, agent_status_cache_db, CACHE_SETTING
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cache import Cache
from flask_oauthlib.client import OAuth
import redis

flaskr = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth()
logger = get_logger("chaos", "INFO", "logs/app.log")
cache = redis.StrictRedis(redis_host, redis_port, db=agent_status_cache_db)
flask_cache = Cache(config=CACHE_SETTING)
gitlab = oauth.remote_app('gitlab',
    base_url=gitlab_base_url,
    request_token_url=None,
    access_token_url=gitlab_access_token_url,
    authorize_url=gitlab_authorize_url,
    access_token_method='POST',
    consumer_key=gitlab_application,
    consumer_secret=gitlab_secret
)


def createApp():
    config = Config()
    flaskr.config.from_object(config)
    db.init_app(flaskr)
    oauth.init_app(flaskr)
    login_manager.init_app(flaskr)
    flask_cache.init_app(flaskr)
    from app.controllers import url as BluePrint
    flaskr.register_blueprint(BluePrint)

    return flaskr


def create_outer_app():
    config = Config()
    flaskr.config.from_object(config)
    flask_cache.init_app(flaskr)
    db.init_app(flaskr)
    return flaskr
