# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify, redirect, url_for
from app.models import Mission, Machine, db
from flask_login import login_required, current_user
from jinja2 import Template
from app.controllers import url
from app import logger, flaskr, flask_cache, cache
from tasks import celery_app
from configer import Config, sample_host, sample_path, sample_data, placeholder_data, placeholder_header, help_on_env, help_on_file, open_admin, activate
from code_templates import result_template, apilist_template
from app.services.missionService import runjob, monitorServer, createMission, parseTest, get_report_born_time
from app.services.commonService import generate_result, get_gitlab_info_by_username, get_gatling_report_dir
from app.services.cacheService import get_all_missions
import time, traceback, os


@url.route("/addmission", methods=["GET", "POST"])
@login_required
def addMission():
    info = {"result": True, "errorMsg": None}
    user_projects = get_gitlab_info_by_username(current_user.nickname)
    if request.method == "POST":
        try:
            mission = createMission(request)
            monitorServer(mission)
            horner = runjob(mission)
            info["relatemachine"] = True if mission.choicedMachines else False
            info["missionid"] = mission.id
            info["machineid"] = mission.choicedMachines[0].id if mission.choicedMachines else 0
            info["job_id"] = horner.job_id
            cache.setex("job_id_%s" % mission.id, 3600 * 24 * 7, horner.job_id)
            db.session.close()
        except Exception as e:
            logger.info("Error Occured: %s %s" % (e, traceback.format_exc()))
            info["result"] = False
            info["errorMsg"] = str(e)
        finally:
            return jsonify(info)

    default_api_template = Template(apilist_template).render(
        id=1,
        placeholder_data=placeholder_data,
        placeholder_header=placeholder_header,
        test_path=sample_path,
        test_data=sample_data,
        helpon=True,
        helponenv=help_on_env,
        helponfile=help_on_file
    )

    machines = Machine.query.filter_by(username=current_user.nickname).all()
    formcode = None
    choiced_api = None
    edit = False

    if request.args.get("edit"):
        edit = True
        mission_id = request.args.get("mission_id")
        mission = Mission.query.filter_by(id=mission_id).first()
        formcode = mission.formcode
        choiced_api = mission.project

    db.session.close()
    return render_template(
        "addMission.html",
        choiced="addMission",
        default_api_template=default_api_template,
        nickname=current_user.nickname,
        machines=machines,
        base_url=sample_host,
        user_projects=user_projects,
        edit=edit,
        formcode=formcode,
        choiced_api=choiced_api
    )


@url.route("/missions")
@login_required
def missions():
    return render_template(
        "missions.html",
        choiced="missions",
        nickname=current_user.nickname
    )


@url.route("/missions/refresh")
def refresh_mission_cache():
    flask_cache.delete("all_missions")
    return redirect(url_for("main.missions"))


@url.route("/missions/tojson")
def get_missions_by_json_format():
    start = int(request.args.get("start"))
    size = int(request.args.get("size"))
    search = request.args.get("search")
    begin = time.time()
    missions = get_all_missions()
    end = time.time()
    logger.info("查询所有任务耗时：%s" % round(end - begin, 3))
    if search:
        missions = [m for m in missions if search in str(m)]
    show_missions = missions[start: start+size]
    page = start / size + 1

    resp = {
        "page": page,
        "rows": show_missions,
        "total": len(missions)
    }
    return jsonify(resp)


@url.route("/jobdetail/<mission_id>/<debug>")
def get_job_detail(mission_id, debug):
    info = {"result": True, "data": None, "finish": False, "details":[]}

    info["data"] = cache.get("mission_%s_log" % mission_id)
    if cache.get("mission_%s_finish" % mission_id):
        info["finish"] = True
        generate_result(mission_id)

    if debug != "false":
        details = {file.split("%s_%s_" % (current_user.nickname, mission_id))[1]: os.path.join("static", "debug_detail", file) for file in os.listdir(Config.DEBUG_DETAIL_FOLDER) if file.startswith("%s_%s_" % (current_user.nickname, mission_id))}
        info["details"] = details or ""

    return jsonify(info)


@url.route("/stop/<mission_id>/<job_id>")
def stopMission(mission_id, job_id):
    info = {"result": True, "errorMsg": None}
    logger.info("terminate job: " + job_id)
    try:
        celery_app.control.revoke(job_id, terminate=True, signal='SIGKILL')
    except Exception as e:
        info["result"] = False
        info["errorMsg"] = str(e)
    logger.info("terminate job success!")
    try:
        m = Mission.query.filter_by(id=mission_id).first()
        m.status = -1
        db.session.add(m)
        db.session.commit()
    except Exception as e:
        info["result"] = False
        info["errorMsg"] = str(e)
    return jsonify(info)


@url.route("/testapi/<int:apiid>", methods=["POST"])
def testApi(apiid):
    info, url, method, body, header, status_code, r_elapsed, r_body, r_headers, envs = parseTest(request, apiid)
    info["message"] = Template(result_template).render(
        url=url,
        method=method,
        req_body=body,
        req_header=header,
        resp_code=status_code,
        resp_elapsed=r_elapsed,
        resp_body=r_body,
        resp_header=r_headers,
        envs=envs
    )

    return jsonify(info)


@url.route("/getapitemplate/<int:id>")
def getApiTemplate(id):
    apilist = Template(apilist_template).render(
        id=id,
        placeholder_data=placeholder_data,
        placeholder_header=placeholder_header
    )
    return apilist


@url.route("/rerun/<int:missionid>", methods=["POST"])
def reRun(missionid):
    info = {"result": True, "errorMsg": None}
    mission = Mission.query.filter_by(id=missionid).first()
    if mission:
        runjob(mission, rerun=True)
    else:
        info["result"] = False
        info["errorMsg"] = "任务不存在或已被删除"
    return jsonify(info)


@url.route("/report/<mission_id>")
def getReport(mission_id):
    try:
        mission = Mission.query.filter_by(id=mission_id).first() if mission_id != "latest" else Mission.query.filter_by(status=1).order_by(Mission.id.desc()).first()
        if mission:
            still_running_msg = "压测仍在进行中，报告尚未生成，客官稍后再来..."
            if mission.loadtool == "jmeter":
                report_path = "static/reports/report-%s/index-%s.html" % (mission.loadtool, mission.id)
                if os.path.exists(os.path.join(flaskr.static_folder.split("/static")[0], report_path)):
                    return redirect(report_path)
            elif mission.loadtool == "gatling":
                if os.path.exists(os.path.join(Config.REPORT_FOLDER, "report-gatling", "report-%s.tar.gz" % mission_id)):
                    report_path = os.path.join(Config.REPORT_FOLDER.split("/app/")[1], get_gatling_report_dir(mission_id), "index.html")
                    return redirect(report_path)
                else:
                    return still_running_msg
            else:
                return still_running_msg
    except Exception as e:
        return "获取报告异常:<br>" + traceback.format_exc().replace("\n", "<br>")

    return "没有运行记录"


@url.route("/edit/<mission_id>")
def editMission(mission_id):
    info = {"result": True, "data": None, "errorMsg": None}
    mission = Mission.query.filter_by(id=mission_id).first()
    if mission:
        info["data"] = mission.formcode

    return jsonify(info)


@url.route("/deletemission/<mission_id>", methods=["DELETE"])
def deletemission(mission_id):
    info = {"result": True, "errorMsg": None}
    mission = Mission.query.filter_by(id=mission_id).first()
    if mission:
        mission.status = -1
        db.session.add(mission)
        db.session.commit()
        db.session.close()
    else:
        info["result"] = False
        info["errorMsg"] = "任务不存在或已被删除"

    return jsonify(info)
