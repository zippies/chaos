# -*- encoding:utf-8 -*-
from code_templates import jmeter_template, gatling_template
from app.services.horn.executor import Horner, Monitor
from app.services.agentService import get_active_agents
from app.models import db, Mission, Machine
from flask_login import current_user
from collections import namedtuple
from configer import Config, enable_distributed_concurrent, activate
from jinja2 import Template
from app import logger, flask_cache
import datetime
import requests
import json
import re

api = namedtuple("api", [
    'Upname',
    'name',
    'method',
    'path',
    'gatling_header',
    'jmeter_header',
    'body',
    'thinktime',
    'envs',
    'check_code',
    'check_body',
    'check_resptime',
    'file',
    'delimiter'
])


def calculateSeconds(duration, durationType):
    seconds = 0
    if duration:
        if durationType == "s":
            seconds = duration
        elif durationType == "m":
            seconds = duration * 60
        elif durationType == "h":
            seconds = duration * 3600
        else:
            pass

    return seconds


def runjob(mission, rerun=False):
    if rerun:
        mission = Mission(
            current_user.nickname,
            mission.project,
            mission.api_name,
            mission.name,
            mission.baseUrl,
            mission.paths,
            mission.types,
            mission.headers,
            mission.bodies,
            mission.concurrent,
            mission.concurrent2,
            mission.loadType,
            mission.duration,
            mission.durationType,
            mission.loopcount,
            mission.script,
            mission.choicedMachines,
            mission.loadtool,
            mission.scheduleron,
            mission.tag,
            mission.formcode,
            mission.ramptime,
            mission.apis,
            mission.gradient,
            mission.agent_count,
            mission.agents
        )
        db.session.add(mission)
        db.session.commit()
        monitorServer(mission)

    dtype = None
    if mission.durationType == "s":
        dtype = "seconds"
    elif mission.durationType == "m":
        dtype = "minutes"
    elif mission.durationType == "h":
        dtype = "hours"
    else:
        dtype = "seconds"

    script = ""
    agents = []
    agent_count = 0
    if mission.loadtool == "gatling":
        baseUrl = mission.baseUrl
        if "http" not in baseUrl:
            baseUrl = "http://" + baseUrl
        script = Template(gatling_template).render(
            user=current_user.nickname,
            className=mission.name,
            apis=mission.apis,
            baseUrl=baseUrl,
            concurrent=mission.concurrent,
            concurrent2=mission.concurrent2,
            loadtype=mission.loadType,
            duration=mission.duration,
            durationType=dtype,
            loopcount=mission.loopcount,
            gradient=mission.gradient.split(",") if mission.gradient else [mission.concurrent]
        )
    elif mission.loadtool == "jmeter":
        agents = [a.get("host") for a in get_active_agents()]
        agent_count = len(agents)

        script = Template(jmeter_template).render(
            user=current_user.nickname,
            missionName=mission.name,
            apis=mission.apis,
            host=mission.baseUrl.split(":")[0],
            port=mission.baseUrl.split(":")[1] if ":" in mission.baseUrl else 80,
            concurrent=mission.concurrent,
            scheduleron=mission.scheduleron,
            duration=mission.duration,
            loopcount=mission.loopcount,
            ramptime=mission.ramptime,
            upload_folder=Config.JMETER_UPLOAD_FOLDER,
            debug_detail_folder=Config.DEBUG_DETAIL_FOLDER,
            mission_id="{{ mission_id }}",
            gradient=mission.gradient.split(",") if mission.gradient else [mission.concurrent],
            enable_distributed_concurrent=enable_distributed_concurrent,
            agent_count=agent_count,
            agent_concurrent=mission.concurrent/agent_count if agent_count else 0
        )
    else:
        pass

    # refresh_missions_cache.apply_async(queue=activate)
    flask_cache.delete("all_missions")
    script = Template(script).render(mission_id=mission.id)
    try:
        mission.script = script
        if not mission.gradient and mission.concurrent >= enable_distributed_concurrent and agent_count:
            mission.agent_count = agent_count
            mission.agents = ",".join(agents)
        db.session.add(mission)
        db.session.commit()
    except Exception as e:
        logger.error("[ERROR]操作数据库更新mission失败")

    horner = Horner(mission.id, mission.name, script, mission.username, mission.loadtool, mission.agents.split(",") if mission.agents else [])
    horner.run()
    return horner


def monitorServer(mission):
    for choicedMachine in mission.choicedMachines:
        monitor = Monitor(
            name=choicedMachine.name,
            missionid=mission.id,
            host=choicedMachine.ip,
            port=choicedMachine.port,
            username=choicedMachine.user,
            frequency=1,
            count=calculateSeconds(mission.duration, mission.durationType) + 30,
            password=choicedMachine.password,
            pkeycontent=choicedMachine.rsa or None,
            timeout=15
        )
        status, errorMsg = monitor.pushFile()
        if not status:
            raise Exception(errorMsg)
        monitor.startMonitor()


def init_multi_datas(request):
    dictform = dict(request.form)
    apicount = len(dictform.get("apiitems"))
    paths, types, gatling_headers, jmeter_headers, bodies, thinktimes, envs, check_codes, check_bodies, check_resptimes, files, \
    apis, delimiters = list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list()
    for i in range(apicount):
        delimiters.append(request.form.get("delimiter-%s" % (i + 1)))
        paths.append(request.form.get("path-%s" % (i + 1)))
        types.append(request.form.get("type-%s" % (i + 1)).lower())
        header = request.form.get("requestheader-%s" % (i + 1))
        tmpheaders = []
        if header:
            for k, v in eval(header).items():
                tmpheaders.append('"%s" -> "%s"' % (k, v))
            gatling_headers.append("Map(%s)" % ",".join(tmpheaders))
            jmeter_headers.append(eval(header))
        else:
            gatling_headers.append(None)
            jmeter_headers.append({})
        bodies.append(request.form.get("requestbody-%s" % (i + 1)) or {})
        thinktimes.append(request.form.get("thinktime-%s" % (i + 1)) or {})
        envcount = len(dict(request.form).get("env-%s" % (i + 1), []))
        envlist = []
        for j in range(envcount):
            envsource = request.form.get("envsource-%s-%s" % (i + 1, j + 1))
            envname = request.form.get("envname-%s-%s" % (i + 1, j + 1))
            envexpression = request.form.get("envexpression-%s-%s" % (i + 1, j + 1))
            envextracttype = request.form.get("envextracttype-%s-%s" % (i + 1, j + 1))

            envlist.append(
                {"source": envsource, "name": envname, "expression": envexpression, "extracttype": envextracttype})
        envs.append(envlist)

        check_codes.append(request.form.get("equal-code-%s" % (i + 1)))
        check_bodies.append(request.form.get("containValue-body-%s" % (i + 1)))
        check_resptimes.append(request.form.get("responseTime-body-%s" % (i + 1)))
    logger.info(envs)
    for i, file in enumerate(request.files.values()):
        if file.filename:
            datafile = "%s/%s_%s" % (Config.UPLOAD_FOLDER, current_user.nickname, file.filename)
            file.save(datafile)
            if request.form.get("loadtool") == "jmeter":
                targetfile = "%s/%s_%s" % (Config.JMETER_UPLOAD_FOLDER, current_user.nickname, file.filename)
                content = None
                with open(datafile, "r") as f:
                    content = f.readlines()
                with open(targetfile, "w") as f:
                    f.writelines(content[1:])
                files.insert(0, (file.filename, content[0].strip().replace(delimiters[i], ",")))
            else:
                files.insert(0, file.filename)
        else:
            files.insert(0, None)

    for i, p in enumerate(paths):
        name = "api_%s" % (i + 1)
        apis.append(
            api(name.upper(),
                name,
                types[i],
                p,
                gatling_headers[i],
                jmeter_headers[i],
                bodies[i],
                thinktimes[i],
                envs[i],
                check_codes[i],
                check_bodies[i],
                check_resptimes[i],
                files[i] if files else None,
                delimiters[i] if delimiters else ","
            )
        )

    return paths, types, gatling_headers, jmeter_headers, bodies, thinktimes, envs, check_codes, check_bodies, check_resptimes, apis


def init_base_datas(data):
    baseUrl = data.get("baseUrl").split("http://")[-1]
    missionName = data.get("missionName")
    project = data.get("project")
    api_name = data.get("api_name")
    loadtool = data.get("loadtool")
    duration = int(data.get("duration")) if data.get("duration") else 0
    durationType = data.get("durationTimeOptions")
    loadtype = data.get("loadType")
    formcode = data.get("formcode")
    concurrent = 0
    concurrent2 = 0
    loopcount = 0
    ramptime = 0
    gradient = ""
    scheduleron = "false"
    front_concurrent = data.get("jmeter-concurrent", "").strip()

    if loadtool == "gatling":
        front_concurrent = data.get("concurrent")
        gradient = front_concurrent if not front_concurrent.isdigit() else ""
        concurrent = int(front_concurrent) if front_concurrent.isdigit() else 0
        concurrent2 = int(data.get("concurrent2")) if data.get("concurrent2") else 0
    elif loadtool == "jmeter":
        gradient = front_concurrent if not front_concurrent.isdigit() else ""
        concurrent = int(front_concurrent) if front_concurrent.isdigit() else 0
        scheduleron = "true" if data.get("looptype") == "duration" else "false"
        loopcount = data.get("jmeter-loop")
        ramptime = data.get("rampTime")
    tag = data.get("tag")

    return baseUrl, missionName, project, api_name, concurrent, concurrent2, duration, durationType, loadtype, tag, loadtool, loopcount, ramptime, scheduleron, formcode, gradient


def createMission(request):
    baseUrl, missionName, project, api_name, concurrent, concurrent2, duration, durationType, loadtype, tag, loadtool, loopcount, ramptime, scheduleron, formcode, gradient = init_base_datas(
        request.form)

    paths, types, gatling_headers, jmeter_headers, bodies, thinktimes, envs, check_codes, check_bodies, check_resptimes, apis = init_multi_datas(
        request)

    choicedMachines = [Machine.query.filter_by(id=mid).first() for mid in dict(request.form).get("machines", [])]

    mission = Mission(
        current_user.nickname,
        project,
        api_name,
        missionName,
        baseUrl,
        paths,
        types,
        gatling_headers if loadtool == "gatling" else jmeter_headers,
        bodies,
        concurrent,
        concurrent2,
        loadtype,
        duration,
        durationType,
        loopcount,
        "",
        choicedMachines,
        loadtool,
        scheduleron,
        tag,
        formcode,
        ramptime,
        apis,
        gradient,
        0,
        ""
    )
    db.session.add(mission)
    db.session.commit()
    return mission


def parseTest(request, apiid):
    info = {"result": True, "errorMsg": None}

    form = request.form
    baseUrl = form.get("baseUrl")
    if "http" not in baseUrl:
        baseUrl = "http://" + baseUrl
    method = form.get("type-%s" % apiid)
    path = form.get("path-%s" % apiid)
    body = form.get("requestbody-%s" % apiid, '{}') or '{}'
    header = form.get("requestheader-%s" % apiid, '{}') or '{}'
    conn_timeout = int(form.get("connectionTimeout-%s" % apiid, 5))
    resp_timeout = int(form.get("responseTimeout-%s" % apiid, 100))
    delimiter = form.get("delimiter-%s" % apiid, ",")
    apicount = len(dict(form).get("apiitems"))
    url = baseUrl + path
    r = None
    data_file = request.files.get("file-%s" % apiid)
    if data_file and data_file.filename:
        datafile = "%s/%s" % (Config.UPLOAD_FOLDER, data_file.filename)
        data_file.save(datafile)
        with open(datafile, "r") as f:
            params = f.readline().strip().split(delimiter)
            data = f.readline().strip().split(delimiter)
            for k, v in zip(params, data):
                body = body.replace("${%s}" % k, v)
                header = header.replace("${%s}" % k, v)
                url = url.replace("${%s}" % k, v)
    try:
        if method.lower() == "post":
            r = requests.post(url=url, data=json.dumps(eval(body)), headers=eval(header), timeout=(conn_timeout, resp_timeout))
        elif method.lower() == "get":
            r = requests.get(url=url, params=eval(body), headers=eval(header), timeout=(conn_timeout, resp_timeout))
        elif method.lower() == "delete":
            r = requests.delete(url=url, data=eval(body), headers=eval(header),
                                timeout=(conn_timeout, resp_timeout))
        elif method.lower() == "put":
            r = requests.put(url=url, data=json.dumps(eval(body)), headers=eval(header), timeout=(conn_timeout, resp_timeout))
        else:
            info["result"] = False
            info["errorMsg"] = "unsupported method"
    except Exception as e:
        r = "接口无返回"

    envs = []

    try:
        if not isinstance(r, str):
            for i in range(apicount):
                envcount = len(dict(form).get("env-%s" % (i + 1), []))
                for j in range(envcount):
                    envsource = form.get("envsource-%s-%s" % (i + 1, j + 1))
                    envname = form.get("envname-%s-%s" % (i + 1, j + 1))
                    envregx = form.get("envregx-%s-%s" % (i + 1, j + 1))
                    logger.info("envsource: %s envname: %s envregx: %s" % (envsource, envname, envregx))
                    reg = re.compile(envregx)
                    env = None
                    if envsource == "header":
                        try:
                            env = reg.search(str(r.headers)).groups()[0]
                        except Exception as e:
                            env = str(e)
                    elif envsource == "body":
                        try:
                            env = reg.search(r.text).groups()[0]
                        except Exception as e:
                            env = str(e)
                    envs.append((envname, env))
    except Exception as e:
        logger.warning("[WARN]:" + str(e))
    r_body = None
    if not isinstance(r, str) and r.headers.get("Content-Type") == "application/json":
        r_body = json.dumps(r.json(), indent=4, ensure_ascii=False)
    elif not isinstance(r, str):
        r_body = r.text
    else:
        r_body = r

    status_code = r.status_code if not isinstance(r, str) else 2000
    r_elapsed = int(r.elapsed.microseconds / 1000) if not isinstance(r, str) else 0
    r_headers = r.headers if not isinstance(r, str) else r
    return info, url, method, body, header, status_code, r_elapsed, r_body, r_headers, envs


def get_report_born_time(mission):
    started_time = mission.createdtime
    duration = mission.duration
    duration_type = mission.durationType
    if duration_type == "s":
        started_time += datetime.timedelta(seconds=duration)
    elif duration_type == "m":
        started_time += datetime.timedelta(minutes=duration)
    elif duration_type == "h":
        started_time += datetime.timedelta(hours=duration)
    else:
        pass
    return started_time.strftime("%Y-%m-%d %H:%M:%S")
