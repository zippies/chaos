# -*- encoding:utf-8 -*-
from app import flask_cache, logger
from app.models import db, Mission, Result
import requests


@flask_cache.cached(key_prefix="all_missions", timeout=-1)
def get_all_missions():
    logger.info("[get_all_missions]未命中缓存")
    missions = [m.json_detail for m in Mission.query.order_by(db.desc("id")).all()]
    return missions


@flask_cache.cached(key_prefix="all_projects", timeout=-1)
def get_gitlab_projects(username, token):
    logger.info("[get_gitlab_projects]未命中缓存 username:%s" % username)
    group_projects = []
    circle = 1
    while True:
        url = "http://git.caimi-inc.com/api/v3/projects?private_token=%s&sudo=%s&page=%s" %(token, username, circle)
        r = requests.get(url, timeout=(10, 30))
        if r.status_code == 200:
            if len(r.json()) == 0:
                break
            else:
                group_projects.extend([p.get("path_with_namespace") for p in r.json()])
        circle += 1

    group_projects = sorted(group_projects, key=lambda x:x.split("/")[0])

    return group_projects


@flask_cache.cached(key_prefix="all_results", timeout=-1)
def get_all_results():
    logger.info("[get_all_results]未命中缓存")
    results = Result.query.all()
    return results