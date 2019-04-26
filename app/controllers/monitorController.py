# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify, abort
from app.models import Machine, Mission
from app.services.horn.executor import Monitor
from flask_login import login_required, current_user
from code_templates import monitor_template
from jinja2 import Template
from configer import monitor_panel_id_list, monitor_url
from app.controllers import url
from app import logger
import time


@url.route("/getMonitorResult")
def getMonitorResult(missionid=None):
    info = {"result": True, "errorMsg": None}
    inner = True if missionid else False

    missionid = request.args.get("missionid") if not missionid else missionid

    mission = Mission.query.filter_by(id=missionid).first()

    if mission:
        if mission.choicedMachines:
            for machine in mission.choicedMachines:
                monitor = Monitor(
                    name=machine.name,
                    missionid=mission.id,
                    host=machine.ip,
                    port=machine.port,
                    username=machine.user,
                    password=machine.password,
                    pkeycontent=machine.rsa or None,
                    timeout=15
                )

                if monitor.isready:
                    result, errorMsg, report_file = monitor.getResult()
                    info["result"] = result
                    info["errorMsg"] = errorMsg
                    info["count"] = len(mission.choicedMachines)
                    info["report_file"] = report_file
                    break
                else:
                    info["result"] = False
                    info["errorMsg"] = "监控数据采集中"
        else:
            info["result"] = False
            info["errorMsg"] = "未关联机器"
    else:
        info["result"] = False
        info["errorMsg"] = "没有运行中的任务"

    return jsonify(info) if not inner else info


@url.route("/viewMonitorReport/<report>")
@login_required
def viewMonitorReport(report):
    return render_template(report)


@url.route("/viewMissionReports/<int:missionid>")
def viewMissionReports(missionid):
    from jinja2 import Template
    mission = Mission.query.filter_by(id=missionid).first()
    if mission:
        report_templates = """
        <div style='padding:50px'>
            <h3>机器监控报告列表</h3>
            <ul>
                {% for machine in machines %}
                    <li><a href="/viewMachineReport/{{ mission.id }}/{{ machine.id }}" target="_blank">{{ machine.id }}-{{ machine.ip}}</a></li>
                {% endfor %}
            </ul>
        </div>
        """
        machines = mission.choicedMachines
        reports = Template(report_templates).render(
            machines=machines,
            mission=mission
        )
        return reports
    else:
        return "没有找到任务"


@url.route("/viewMachineReport/<int:missionid>/<int:machineid>")
@login_required
def viewMachineReport(missionid, machineid):
    logger.info("%s 查看报告,mission_id: %s" % (current_user.nickname, missionid))
    mission = Mission.query.filter_by(id=missionid).first()
    machine = Machine.query.filter_by(id=machineid).first()
    if mission:
        result = getMonitorResult(mission.id)
        logger.info("result: %s" % result)
        if result["result"]:
            return render_template("%s_%s.html" % (machine.name, missionid))
        else:
            abort(404)
    else:
        abort(404)


@url.route("/monitor/add")
def add_monitor():
    namespace = request.args.get("namespace")
    instance_name = request.args.get("instance_name")
    base_url = request.args.get("base_url")

    panel_list = monitor_panel_id_list.split(",")
    wai = "wai-"
    if "wac-ai" not in base_url:
        wai = ""

    url_list = []

    for panel_id in panel_list:
        url = monitor_url.format(
            wai=wai,
            namespace=namespace,
            instance_name=instance_name,
            panel_id=panel_id
        )
        url_list.append(url)

    return Template(monitor_template).render(
        url_list=url_list,
        timestamp=int(time.time()),
        namespace=namespace,
        instance_name=instance_name
    )
