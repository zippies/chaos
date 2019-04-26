# -*- coding: utf-8 -*-
from lib.commons import replace_week
from datetime import datetime
from app import db, login_manager, cache
from flask_login import UserMixin
from jinja2 import Template

info = {"result": True, "errorMsg": None}


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


login_manager.session_protection = "strong"
login_manager.login_view = "main.login"
login_manager.login_message = {"type": "error", "message": "请登录后使用该功能"}


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(32))
    token = db.Column(db.String(128))
    ip = db.Column(db.String(64))
    createdtime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, nickname, token, ip):
        self.nickname = nickname
        self.token = token
        self.ip = ip

    def to_json(self):
        return {
            "name": self.nickname,
            "createdtime": self.createdtime
        }

    def __repr__(self):
        return "<User:%s>" % self.nickname


class UserProjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    projects = db.Column(db.Text)
    createdtime = db.Column(db.DateTime, default=datetime.now)
    updatedtime = db.Column(db.DateTime, onupdate=datetime.now)

    def __init__(self, username, projects):
        self.username = username
        self.projects = projects


class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    project = db.Column(db.String(64))
    api_name = db.Column(db.String(64))
    baseUrl = db.Column(db.String(128))
    paths = db.Column(db.PickleType)
    types = db.Column(db.PickleType)
    headers = db.Column(db.PickleType)
    bodies = db.Column(db.PickleType)
    concurrent = db.Column(db.Integer)
    concurrent2 = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    durationType = db.Column(db.String(10))
    loopcount = db.Column(db.Integer)
    loadType = db.Column(db.String(32))
    script = db.Column(db.PickleType)
    status = db.Column(db.Integer, default=0) # -1: 已停止  0：运行中 1: 已完成
    username = db.Column(db.String(32))
    machineid = db.Column(db.Integer)
    choicedMachines = db.Column(db.PickleType)
    loadtool = db.Column(db.String(32))
    scheduleron = db.Column(db.String(10))
    tag = db.Column(db.String(32), default="tag")
    formcode = db.Column(db.Text)
    ramptime = db.Column(db.Integer)
    apis = db.Column(db.PickleType)
    gradient = db.Column(db.String(256))
    agent_count = db.Column(db.Integer)
    agents = db.Column(db.String(512))
    createdtime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, project, api_name, name, baseUrl, paths, types, headers, bodies, concurrent,
                 concurrent2, loadType, duration, durationType, loopcount, script, choicedMachines, loadtool,
                 scheduleron, tag, formcode, ramptime, apis, gradient, agent_count, agents):
        self.username = username
        self.project = project
        self.api_name = api_name.strip()
        self.name = name.strip()
        self.baseUrl = baseUrl
        self.paths = paths
        self.types = types
        self.headers = headers
        self.bodies = bodies
        self.concurrent = int(concurrent)
        self.concurrent2 = int(concurrent2)
        self.loadType = loadType
        self.duration = int(duration)
        self.durationType = durationType
        self.loopcount = loopcount
        self.script = script
        self.choicedMachines = choicedMachines
        self.loadtool = loadtool
        self.scheduleron = scheduleron
        self.tag = tag
        self.formcode = formcode
        self.ramptime = ramptime
        self.apis = apis
        self.gradient = gradient
        self.agent_count = agent_count
        self.agents = agents

    def to_json(self):
        return {
            "id": self.id,
            "tag": self.tag,
            "createdtime": replace_week(self.createdtime.strftime("%Y-%m-%d %H:%M:%S (%A)")),
        }

    @property
    def json_detail(self):
        paths = Template("""{% for path in paths %}<pre>[{{ types[loop.index-1] }}] {{ path }} </pre>{% endfor %}""").render(
            paths=self.paths,
            types=self.types
        )
        concurrent = Template("""{{ concurrent or gradient }}{% if loadType not in ['atOnceUsers','rampUsers','constantUsersPerSec'] %} ~ {{ concurrent2 }}{% endif %}""").render(
            concurrent=self.concurrent,
            concurrent2=self.concurrent2,
            gradient=self.gradient,
            loadType=self.loadType
        )
        duration = Template("""{% if loadtool == "jmeter" %}{% if scheduleron == "true" %}{{ loopcount }} s{% else %}{{ loopcount }}次{% endif %}{% else %}{{ duration }} {{ durationType }}{% endif %}""").render(
            loadtool=self.loadtool,
            scheduleron=self.scheduleron,
            loopcount=self.loopcount,
            duration=self.duration,
            durationType=self.durationType
        )
        loadtype = Template("""{% if loadtool == "jmeter" %}jmeter{% else %}{{ loadType }}{% endif %}""").render(
            loadtool=self.loadtool,
            loadType=self.loadType
        )
        operation = Template("""
                        <div class="btn-group">
                            <button class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                更多 <span class="caret"></span>
                            </button>
                            <ul class="dropdown-menu">
                                <li><a href="/addmission?edit=true&mission_id={{ id }}">编辑</a></li>
                                {% if status == 0 %}
                                    <li><a href="javascript:void(0);" onclick="stop({{ id }}, '{{ job_id }}')">停止运行</a></li>
                                {% elif status == 1%}
                                    <li><a href="javascript:void(0);" onclick="rerun({{ id }})">重新运行</a></li>
                                    <li role="separator" class="divider"></li>
                                    {% if choicedMachines %}<li><a href="/viewMissionReports/{{ id }}" target="_blank">查看监控报告</a></li>{% endif %}
                                    <li><a href="/report/{{ id }}" target="_blank">查看性能报告</a></li>
                                {% endif %}
                            </ul>
                        </div>""").render(
            choicedMachines=self.choicedMachines,
            id=self.id,
            job_id=cache.get("job_id_%s" % self.id),
            status=self.status
        )
        return {
            "id": self.id,
            "project": "<pre>%s</pre>" % self.project,
            "api_name": "<pre>%s</pre>" % self.api_name,
            "paths": paths,
            "concurrent": "<pre>%s</pre>" % concurrent,
            "duration": duration,
            "tag": "<pre>%s</pre>" % (self.tag.strip() or "无"),
            "loadtype": "<pre>%s</pre>" % loadtype,
            "createdtime": "<pre>%s</pre>" % self.createdtime.strftime("%Y-%m-%d %H:%M:%S"),
            "creator": self.username,
            "operation": operation
        }

    @property
    def short_paths(self):
        return [i[:35] for i in self.paths]

    @property
    def has_report(self):
        report = Result.query.filter_by(mission_id=self.id).first()
        return report is not None

    def __repr__(self):
        return "<Mission:%s>" % self.name


class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    ip = db.Column(db.String(64))
    sshtype = db.Column(db.String(16))
    user = db.Column(db.String(32))
    port = db.Column(db.Integer)
    password = db.Column(db.String(32))
    rsa = db.Column(db.String(5000))
    memory = db.Column(db.String(20))
    cpu = db.Column(db.Integer)
    disk = db.Column(db.String(20))
    username = db.Column(db.String(32))
    createdtime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name, ip, sshtype, user, port, password, rsa, memory, cpu, disk, username):
        self.name = name
        self.ip = ip
        self.sshtype = sshtype
        self.user = user
        self.port = port
        self.password = password
        self.rsa = rsa
        self.memory = memory
        self.cpu = cpu
        self.disk = disk
        self.username = username

    def __repr__(self):
        return "<Machine:%s>" % self.name


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(64))
    api_name = db.Column(db.String(64))
    concurrent = db.Column(db.Integer)
    avg_rt = db.Column(db.String(32))
    min_rt = db.Column(db.String(32))
    max_rt = db.Column(db.String(32))
    rt_p50 = db.Column(db.String(32))
    rt_p75 = db.Column(db.String(32))
    rt_p95 = db.Column(db.String(32))
    rt_p99 = db.Column(db.String(32))
    f_rate = db.Column(db.String(32))
    samples = db.Column(db.Integer)
    ok = db.Column(db.Integer)
    ko = db.Column(db.Integer)
    tps = db.Column(db.Float, default=0.0)
    mission_id = db.Column(db.Integer)
    createdtime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, project, api_name, concurrent, avg_rt, min_rt, max_rt, rt_p50, rt_p75, rt_p95, rt_p99, f_rate, samples, ok, ko, tps, mission_id):
        self.project = project
        self.api_name = api_name
        self.concurrent = concurrent
        self.avg_rt = avg_rt
        self.min_rt = min_rt
        self.max_rt = max_rt
        self.rt_p50 = rt_p50
        self.rt_p75 = rt_p75
        self.rt_p95 = rt_p95
        self.rt_p99 = rt_p99
        self.f_rate = f_rate
        self.samples = samples
        self.ok = ok
        self.ko = ko
        self.tps = tps
        self.mission_id = mission_id

    @property
    def tag(self):
        mission = Mission.query.filter_by(id=self.mission_id, status=0).first()
        if mission:
            return mission.tag
        else:
            return ""

    @property
    def gradient(self):
        mission = Mission.query.filter_by(id=self.mission_id, status=0).first()
        if mission:
            return mission.gradient
        else:
            return ""

    @property
    def is_deleted(self):
        mission = Mission.query.filter_by(id=self.mission_id, status=0).first()
        if mission:
            print "no mission found"
            return False
        else:
            print "find mission"
            return True

    @property
    def mission_createdtime(self):
        mission = Mission.query.filter_by(id=self.mission_id).first()
        if mission:
            return mission.createdtime
        else:
            return datetime.now()

    def __repr__(self):
        return "<Result_Mission:%s_%s>" % (self.id, self.mission_id)