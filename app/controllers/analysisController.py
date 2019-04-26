# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify, redirect, url_for
from app.models import Mission, db
from lib.commons import replace_week
from flask_login import current_user, login_required
from app.services.cacheService import get_all_results
from app.controllers import url
from app import logger, flask_cache
import json
import time


@url.route("/analyze/refresh")
def refresh_analyze_cache():
    flask_cache.delete("all_results")
    return redirect(url_for("main.analyzePerformance"))


@url.route("/analyze", methods=["GET", "POST"])
@login_required
def analyzePerformance():
    project = api_name = concurrent = ""
    start = time.time()
    results = get_all_results()
    end = time.time()
    logger.info("[get_all_results]耗时:%s count:%s" % (round(end - start, 3), len(results)))
    projects = list(set([r.project for r in results]))
    mission_ids = []
    if request.method == "POST":
        project = request.form.get("project")
        api_name = request.form.get("api_name")
        concurrent = request.form.get("concurrent")
        mission_ids = dict(request.form).get("mission_ids")
    else:
        if results:
            project = results[-1].project
            api_name = results[-1].api_name
            concurrent = results[-1].gradient or str(results[-1].concurrent)
    if concurrent.isdigit():
        results = [r for r in results if
                   r.project == project and r.api_name == api_name and r.concurrent == int(concurrent)]
    else:
        results = [r for r in results if r.project == project and r.api_name == api_name and r.gradient == concurrent]
    # results 默认与最近一次压测的项目名、接口名和并发数相同的所有报告
    if mission_ids:
        # 默认值时不会到该逻辑
        results = [r for r in results if str(r.mission_id) in mission_ids]

    # 默认值时为全部报告的mission_id
    mission_ids = [r.mission_id for r in results]

    timelist, min_rt_list, max_rt_list, avg_rt_list, avg_rt_p50_list, avg_rt_p75_list, avg_rt_p95_list, avg_rt_p99_list, f_rate_list, tps_list = [], [], [], [], [], [], [], [], [], []

    for result in results:
        timelist.append('%s_%s' % (
        result.tag or "tag", replace_week(result.mission_createdtime.strftime("%Y-%m-%d %H:%M:%S (%A)"))))
        min_rt_list.append('%s' % round(float(result.min_rt), 2))
        max_rt_list.append('%s' % round(float(result.max_rt), 2))
        avg_rt_list.append('%s' % round(float(result.avg_rt), 2))
        avg_rt_p50_list.append('%s' % round(float(result.rt_p50), 2))
        avg_rt_p75_list.append('%s' % round(float(result.rt_p75), 2))
        avg_rt_p95_list.append('%s' % round(float(result.rt_p95), 2))
        avg_rt_p99_list.append('%s' % round(float(result.rt_p99), 2))
        f_rate_list.append('%s' % result.f_rate)
        tps_list.append('%s' % round(float(result.tps), 2) or 0.0)
    start1 = time.time()
    apis = get_apis_by_project_name(project)
    end1 = time.time()
    logger.info("[get_apis_by_project_name]耗时:%s" % round(end1 - start1, 3))
    start2 = time.time()
    concurrents = get_concurrents_by_api_name(api_name)
    end2 = time.time()
    logger.info("[get_concurrents_by_api_name]耗时:%s" % round(end2 - start2, 3))
    start3 = time.time()
    # 与最近一次压测的项目名、接口名和并发数相同的所有mission
    missions = get_missions_by_project_api_concurrent(project, api_name, concurrent)
    end3 = time.time()
    logger.info("[get_missions_by_project_api_concurrent]耗时:%s" % round(end3 - start3, 3))
    logger.info("[analysis]总耗时:%s" % round(end3 - start, 3))
    return render_template(
        "analyze.html", user_projects=projects, project=project, apis=apis, nickname=current_user.nickname,
        api_name=api_name, concurrents=concurrents, concurrent=concurrent, missions=missions,
        mission_ids=mission_ids, timelist=json.dumps(timelist), min_rt_list=json.dumps(min_rt_list),
        max_rt_list=json.dumps(max_rt_list), avg_rt_list=json.dumps(avg_rt_list),
        avg_rt_p50_list=json.dumps(avg_rt_p50_list), avg_rt_p75_list=json.dumps(avg_rt_p75_list),
        avg_rt_p95_list=json.dumps(avg_rt_p95_list), avg_rt_p99_list=json.dumps(avg_rt_p99_list),
        f_rate_list=json.dumps(f_rate_list), tps_list=tps_list, choiced="analyze"
    )


def get_missions_by_project_api_concurrent(project, api_name, concurrent):
    if concurrent.isdigit():
        missions = Mission.query.filter_by(project=project, api_name=api_name, concurrent=concurrent,
                                           status=0).order_by(db.desc("id")).all()
    else:
        missions = Mission.query.filter_by(project=project, api_name=api_name, gradient=concurrent, status=0).order_by(
            db.desc("id")).all()

    return [i.to_json() for i in missions if i.has_report]


def get_apis_by_project_name(project):
    results = get_all_results()
    return list(set([r.api_name for r in results if r.project == project]))


def get_concurrents_by_api_name(api_name):
    results = get_all_results()
    return sorted(list(set([r.gradient or str(r.concurrent) for r in results if r.api_name == api_name])))


@url.route("/apis/<project_name>")
def get_apis_by_project(project_name):
    info = {"result": True, "data": None, "errorMsg": None}
    try:
        info["data"] = get_apis_by_project_name(project_name.replace("||", "/"))
    except Exception as e:
        info["result"] = False
        info["errorMsg"] = str(e)

    return jsonify(info)


@url.route("/concurrents/<api_name>")
def get_concurrents_by_api(api_name):
    info = {"result": True, "data": None, "errorMsg": None}
    try:
        info["data"] = get_concurrents_by_api_name(api_name)
    except Exception as e:
        info["result"] = False
        info["errorMsg"] = str(e)

    return jsonify(info)


@url.route("/missions/<project_name>/<api_name>/<concurrent>")
def get_mission_by_project_api_and_concurrent(project_name, api_name, concurrent):
    info = {"result": True, "data": None, "errorMsg": None}
    try:
        info["data"] = get_missions_by_project_api_concurrent(project_name.replace("||", "/"), api_name, concurrent)
    except Exception as e:
        info["result"] = False
        info["errorMsg"] = str(e)

    return jsonify(info)
