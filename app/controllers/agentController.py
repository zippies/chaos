# -*- encoding:utf-8 -*-
from app.services.commonService import ServiceResponse, local_save, local_get
from app.services.agentService import get_active_agents, get_host_ip
from flask_login import current_user, login_required
from agent import celery_agent
from configer import agent_tag, enable_distributed_concurrent
from app.controllers import url
from app import logger, cache
from flask import jsonify, request, render_template
import traceback
import requests
import json


@url.route("/agents")
@login_required
def agents():
    agents = get_active_agents()

    return render_template("agents.html", choiced="agents", agents=agents, nickname=current_user.nickname)


# ++++++++++++++++++++++++++++++++++++ local agent ++++++++++++++++++++++++++++++++++++++++++ #
@url.route("/agent/start")
def start_agent():
    exec("""from agent import {func_name} as agent_task""".format(func_name=agent_tag))
    agent = agent_task.apply_async(queue=agent_tag)
    local_save("agent_task_id", agent.id)
    return jsonify(ServiceResponse.success({"agent_id": agent.id, "host": get_host_ip()}))


@url.route("/agent/stop")
def stop_agent():
    agent_task_id = local_get("agent_task_id") or 0
    try:
        logger.info("terminate job: %s" % agent_task_id)
        celery_agent.control.revoke(agent_task_id, terminate=True, signal='SIGKILL')
        cache.delete("agents")
        logger.info("terminate job success")
    except Exception as e:
        logger.error(traceback.format_exc())
        return jsonify(ServiceResponse.error(str(e)))

    return jsonify(ServiceResponse.success(data={"agent_task_id": agent_task_id, "host": get_host_ip()}))


# ++++++++++++++++++++++++++++++++++++ remote agent ++++++++++++++++++++++++++++++++++++++++++ #
@url.route("/agent/report/<host>")
def agent_report(host):
    try:
        agent = {
            "cpu": request.args.get("cpu"),
            "memory": request.args.get("memory"),
            "disk": request.args.get("disk"),
            "tag": request.args.get("tag"),
            "host": host,
            "starttime": request.args.get("starttime")
        }
        import time
        cache.set("%s_heartbeat" % host, time.time())
        agents = json.loads(cache.get("agents") or "[]")
        agents = [a for a in agents if time.time() - float(cache.get("%s_heartbeat" % a.get("host"))) < 20 and a.get("host") != host ]
        agents.append(agent)
        cache.set("agents", json.dumps(agents))
        cache.expire("agents", 10)
        return jsonify(ServiceResponse.success({"agents": agents}))
    except Exception as e:
        return jsonify(ServiceResponse.error({"errorMsg": str(e)}))


@url.route("/agent/list")
def agent_list():
    agents = get_active_agents()
    concurrent = request.args.get("concurrent", 0)
    if concurrent and "," not in str(concurrent):
        return jsonify({"enable_distributed": int(concurrent) >= enable_distributed_concurrent, "agents": agents})
    return jsonify(agents)


@url.route("/agent/stop_remote/<host>")
def stop_remote(host):
    hosts = [host]
    if host == "all":
        hosts = [a.get("host") for a in get_active_agents()]
    try:
        for host in hosts:
            r = requests.get("http://{host}:8080/agent/stop".format(host=host), timeout=(2, 3))
            assert r.status_code == 200, "[%s]停止[%s]失败" % (r.status_code, host)
            assert r.json().get("code") == 0, r.json().get("errorMsg")
        return jsonify(ServiceResponse.success())
    except Exception as e:
        return jsonify(ServiceResponse.error(str(e)))
