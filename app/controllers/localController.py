# -*- encoding:utf-8 -*-
from flask import redirect, request, render_template, jsonify
from app.controllers import url
from app.models import User, db
from flask_login import login_user, logout_user


@url.route("/")
@url.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        nickname = request.form.get("nickname")
        user = User.query.filter_by(nickname=nickname).first()
        if not user:
            user = User(nickname, "123456", "127.0.0.1")
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect("addmission?user")

    return render_template("login.html")


@url.route("/users")
def users():
    users = [user.to_json() for user in User.query.all()]
    data = {
        "total": len(users),
        "users": users
    }
    return jsonify(data)


@url.route("/logout")
def logout():
    logout_user()
    return redirect("login")


@url.errorhandler(404)
def page_not_found(error):
    return "指定页面不存在或尚未生成", 404
