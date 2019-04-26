# -*- coding: utf-8 -*-
from flask import request, session, redirect, url_for, jsonify
from flask_login import login_user
from app.models import db, User
from app.controllers import url
from tasks import refresh_projects_cache
from configer import activate
from app import gitlab


@url.route("/check_backend_active.html")
def nginx_check():
    return "i'm ok"


@url.route('/')
def index(relogin=False):
    if 'gitlab_token' in session:
        me = gitlab.get('user')
        user = User.query.filter_by(nickname=me.data.get("email").split("@")[0]).first()
        if not user:
            user = User(
                nickname=me.data.get("email").split("@")[0],
                token=me.data.get("private_token"),
                ip=request.remote_addr
            )
            db.session.add(user)
            db.session.commit()
        else:
            refresh_projects_cache.apply_async(args=[user.nickname, user.token], queue=activate)
        login_user(user)
        return redirect(url_for("main.addMission"))
    return redirect(url_for('main.login'))


@url.route("/users")
def users():
    users = [user.to_json() for user in User.query.all()]
    return jsonify(users)


@url.route('/login')
def login():
    return gitlab.authorize(callback=url_for('main.authorized', _external=True, _scheme='http'))


@url.route('/login/authorized')
def authorized():
    resp = gitlab.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    session['gitlab_token'] = (resp['access_token'], '')
    return redirect(url_for('main.index'))


@gitlab.tokengetter
def get_gitlab_oauth_token():
    return session.get('gitlab_token')


@url.errorhandler(404)
def page_not_found(error):
    return "指定页面不存在或尚未生成", 404
