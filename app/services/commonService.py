# -*- encoding:utf-8 -*-
from app.models import Result, db, Mission, User
from app.services.cacheService import get_gitlab_projects
from configer import domino_url, Config, wechat_notice_url, master_host_port
from code_templates import jmeter_report_template_dict
from app import logger, cache
from jinja2 import Template
import requests
import tarfile
import socket
import json
import time
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

status_path = os.path.join(Config.status_dir, "local.json")


class Domino(object):
    def __init__(self):
        pass

    @staticmethod
    def save(file_path, filename):
        url = domino_url + "/fastupload/chaos"
        files = {"file": open(file_path, "rb")}
        r = requests.post(url, files=files, data={"filename": filename, "expireSeconds": 3600})
        assert r.status_code == 200, "上传异常:" + r.reason

    @staticmethod
    def get(filename, save=False, unzip=False, savepath=""):
        url = domino_url + "/fastdownload/chaos/" + filename
        r = requests.get(url)
        assert r.status_code == 200, "下载异常:" + r.reason
        filepath = os.path.join(Config.REPORT_FOLDER, savepath, filename)
        if save:
            with open(filepath, "wb") as f:
                f.write(r.content)
            if unzip:
                with tarfile.open(filepath, "r:gz") as tar:
                    file_names = tar.getnames()
                    for file_name in file_names:
                        tar.extract(file_name, os.path.join(Config.REPORT_FOLDER, savepath))
        return r.content


def send_wechat_notice(mission_id, user):
    data = {
        "touser" : ",".join([user, "suihouzhu"]),
        "from" : "Chaos- 性能报告已生成",
        "type" : "wechat",
        "content" : "查看报告: http://%s/report/%s" % (master_host_port, mission_id)
    }

    r = requests.post(wechat_notice_url, json=data)
    logger.info("send_wechat:%s %s" % (r.status_code, r.json()))


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def local_save(key, value):
    status = None
    if os.path.exists(status_path):
        status = json.load(open(status_path, "rb"))
        status[key] = value
    else:
        status = {key: value}
    json.dump(status, open(status_path, "wb"))


def local_get(key):
    if os.path.exists(status_path):
        status = json.load(open(status_path, "rb"))
        return status.get(key)
    else:
        return None


class ServiceResponse(object):
    code = 0
    data = None
    errorMsg = None

    @staticmethod
    def error(errorMsg, code=1, data=None):
        return {
            "code": code,
            "data": data,
            "errorMsg": errorMsg
        }

    @staticmethod
    def success(data=None):
        return {
            "code": ServiceResponse.code,
            "data": data,
            "errorMsg": ServiceResponse.errorMsg
        }


def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def get_gitlab_info_by_username(username):
    user = User.query.filter_by(nickname=username).first()
    start = time.time()
    group_projects = get_gitlab_projects(username, user.token)
    end = time.time()
    logger.info("[get_gitlab_info_by_username] user:%s 耗时:%s" % (username, round(end - start, 3)))
    return group_projects


def get_gatling_report_dir(mission_id):
    report_dir = [report_dir for report_dir in os.listdir(Config.REPORT_FOLDER) if
                  report_dir.startswith("report-%s" % mission_id)][0]
    return report_dir


def generate_result(mission_id):
    mission = Mission.query.filter_by(id=mission_id).first()
    if mission:
        avg_rt, min_rt, max_rt, rt_p50, rt_p75, rt_p95, rt_p99, f_rate, samples, ok, ko, tps = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0
        if mission.loadtool == "gatling":
            Domino.get("report-%s.tar.gz" % mission_id, save=True, unzip=True, savepath="report-gatling")
            stat = json.loads(cache.get("mission_%s_stats" % mission_id))
            api = stat.get("stats")
            samples = api.get("numberOfRequests").get("total")
            ok = api.get("numberOfRequests").get("ok")
            ko = api.get("numberOfRequests").get("ko")
            f_rate = round(float(ko) / ok * 100, 1) if ok else 100
            min_rt = api.get("minResponseTime").get("ok")
            max_rt = api.get("maxResponseTime").get("ok")
            avg_rt = api.get("meanResponseTime").get("ok")
            rt_p50 = api.get("percentiles1").get("ok")
            rt_p75 = api.get("percentiles2").get("ok")
            rt_p95 = api.get("percentiles3").get("ok")
            rt_p99 = api.get("percentiles4").get("ok")
        elif mission.loadtool == "jmeter":
            dashboard = cache.get("dashboard_js-%s" % mission_id)
            graph = cache.get("graph_js-%s" % mission_id)
            with open(os.path.join(Config.REPORT_FOLDER, "report-jmeter", "content", "js", "dashboard-%s.js" % mission_id), "wb") as f:
                f.write(dashboard)
            with open(os.path.join(Config.REPORT_FOLDER, "report-jmeter", "content", "js", "graph-%s.js" % mission_id), "wb") as f:
                f.write(graph)
            for page in ["OverTime", "ResponseTimes", "Throughput"]:
                with open(os.path.join(Config.REPORT_FOLDER, "report-jmeter", "content", "pages", "%s-%s.html" % (page, mission_id)), "wb") as f:
                    f.write(Template(jmeter_report_template_dict.get(page)).render(mission_id=mission_id))
            with open(os.path.join(Config.REPORT_FOLDER, "report-jmeter", "index-%s.html" % mission_id), "wb") as f:
                f.write(Template(jmeter_report_template_dict.get("jmeter_report_index_template")).render(mission_id=mission_id))
            stat = json.loads(dashboard.split("statisticsTable\"), ")[1].split(", function")[0])
            api = stat.get("overall").get("data")
            samples = api[1]
            ko = api[2]
            ok = samples - ko
            f_rate = round(api[3], 1)
            min_rt = api[5]
            max_rt = api[6]
            avg_rt = api[4]
            rt_p50 = 0
            rt_p75 = 0
            rt_p95 = api[8]
            rt_p99 = api[9]
            tps = api[10]

        result = Result(
            mission.project, mission.api_name, mission.concurrent, avg_rt, min_rt, max_rt, rt_p50, rt_p75,
            rt_p95, rt_p99, f_rate, samples, ok, ko, tps, mission_id
        )
        mission.status = 1
        db.session.add(result)
        db.session.add(mission)
        db.session.commit()
        db.session.close()


if __name__ == "__main__":
    # get_gitlab_info_by_username("suihouzhu")
    pass
