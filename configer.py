# -*- coding: utf-8 -*-
import ConfigParser
import socket
import re
import os

real_conf = "/tmp/chaos-conf/chaos.cfg"
conf = ConfigParser.ConfigParser()
if os.path.exists(real_conf):
    conf.read(real_conf)
else:
    conf.read("chaos.cfg")

activate = conf.get("main", "activate")
open_admin = conf.getboolean("main", "open_admin")
agent_tag = re.sub("\W", "_", "%s_%s" % (socket.gethostname(), conf.get("main", "agent_tag")))
enable_distributed_concurrent = conf.getint("main", "enable_distributed_concurrent")

master_host_port = conf.get("common-%s" % activate, "master_host_port")
domino_url = conf.get("common-%s" % activate, "domino_url")
wechat_notice_url = conf.get("common-%s" % activate, "wechat_notice_url")

gitlab_base_url = conf.get("gitlab-common", "base_url")
gitlab_access_token_url = conf.get("gitlab-common", "access_token_url")
gitlab_authorize_url = conf.get("gitlab-common", "authorize_url")
gitlab_application = conf.get("gitlab-%s" % activate, "application_id")
gitlab_secret = conf.get("gitlab-%s" % activate, "secret")

redis_host = conf.get("redis-%s" % activate, "host")
redis_port = conf.get("redis-%s" % activate, "port")

master_broker_db = conf.get("redis-common", "master_broker_db")
master_backend_db = conf.get("redis-common", "master_backend_db")
agent_broker_db = conf.get("redis-common", "agent_broker_db")
agent_backend_db = conf.get("redis-common", "agent_backend_db")
agent_status_cache_db = conf.get("redis-common", "agent_status_cache_db")

sample_host = conf.get("mission-sample-%s" % activate, "sample_host")
sample_path = conf.get("mission-sample-%s" % activate, "sample_path")
sample_data = conf.get("mission-sample-%s" % activate, "sample_data")

amusement = conf.get("mission-sample", "amusement")

placeholder_data = conf.get("mission-sample", "placeholder_data")
placeholder_header = conf.get("mission-sample", "placeholder_header")

help_on_env = conf.get("mission-sample", "help_on_env")
help_on_file = conf.get("mission-sample", "help_on_file")

monitor_panel_id_list = conf.get("monitor-%s" % activate, "panel_id_list")
monitor_url = conf.get("monitor-%s" % activate, "url")

CACHE_SETTING = {
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_HOST": redis_host,
    "CACHE_REDIS_PORT": redis_port,
    "CACHE_REDIS_DB": master_broker_db,
    "CACHE_REDIS_PASSWORD": ""
}


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db', 'data.sqlite')
    SECRET_KEY = 'what does the fox say?'
    WTF_CSRF_SECRET_KEY = "whatever"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CAS_SERVER = "http://host:port"
    CAS_AFTER_LOGIN = "addmission"
    CAS_VALIDATE_ROUTE = "/serviceValidate"
    SQLALCHEMY_POOL_RECYCLE = 5

    GATLING_HOME = os.path.join(os.path.dirname(__file__), "gatling2.3.1")

    UPLOAD_FOLDER = os.path.join(GATLING_HOME, "user-files", "data")

    SCRIPT_FOLDER = os.path.join(GATLING_HOME, "user-files", "simulations")

    JMETER_HOME = os.path.join(os.path.dirname(__file__), "apache-jmeter-3.3")

    JMETER_SCRIPT_FOLDER = os.path.join(JMETER_HOME, "scripts")

    JMETER_UPLOAD_FOLDER = os.path.join(JMETER_HOME, "uploads")

    REPORT_FOLDER = os.path.join(os.path.dirname(__file__), "app", "static", "reports")

    DEBUG_DETAIL_FOLDER = os.path.join(os.path.dirname(__file__), "app", "static", "debug_detail")

    bin_path = os.path.join(os.path.dirname(__file__), "bin")

    nmon_file_path = os.path.join(bin_path, "nmon")

    machine_report_dir = os.path.join(os.path.dirname(__file__), "app", "templates")

    nmon_file_dir = os.path.join(os.path.dirname(__file__), "app", "static", "nmon_files")

    status_dir = os.path.join(os.path.dirname(__file__), "logs")

    @staticmethod
    def init_app(app):
        pass

if __name__ == "__main__":
    print agent_tag
