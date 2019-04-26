# -*- encoding:utf-8 -*-
from kombu import Exchange, Queue
from lib.logger import get_logger
from app.services.cacheService import get_gitlab_projects
from app.services.commonService import Domino, get_gatling_report_dir, send_wechat_notice
from app import flask_cache, create_outer_app, cache
from configer import Config, redis_host, redis_port, master_broker_db, master_backend_db, activate
from celery import Celery
import traceback
import pexpect
import tarfile
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

celery_app = Celery(
    "chaos_worker",
    backend="redis://{host}:{port}/{db}".format(host=redis_host, port=redis_port, db=master_broker_db),
    broker="redis://{host}:{port}/{db}".format(host=redis_host, port=redis_port, db=master_backend_db)
)
celery_app.conf.timezone = 'UTC'

queue = set()
route = dict()

queue.add(Queue(activate, Exchange("Exchange", type="direct"), routing_key="%s_key" % activate))
route["tasks.%s" % activate] = {"queue": activate, "routing_key": "%ss_key" % activate}

celery_app.conf.update(task_queues=queue, task_routes=route)


@celery_app.task
def refresh_projects_cache(username, token):
    with create_outer_app().app_context():
        flask_cache.delete("all_projects")
        get_gitlab_projects(username, token)
    return "刷新gitlab_projects缓存成功, user:%s" % username


@celery_app.task
def worker_run_job(loadtool, user, script_name, script, mission_id, agent_list=list()):
    logger = get_logger("job", "INFO", "logs/job_%s.log" % mission_id)

    def create_script():
        folder = os.path.join(
            Config.SCRIPT_FOLDER if loadtool == "gatling" else Config.JMETER_SCRIPT_FOLDER,
            user
        )
        if loadtool == "jmeter":
            report_folder = os.path.join(
                Config.REPORT_FOLDER, "report-{mission_id}-jmeter".format(mission_id=mission_id)
            )
            os.makedirs(report_folder)
        if not os.path.exists(folder):
            os.makedirs(folder)

        filename = os.path.join(folder, "%s.%s" % ("%s-%s" % (script_name, mission_id) if loadtool != "gatling" else script_name, "scala" if loadtool == "gatling" else "jmx"))

        with open(filename, "wb") as f:
            f.write(script)

    def save_to_remote(js_dir, mission_id, save_list):
        try:
            for file in save_list:
                with open(os.path.join(js_dir, file), "rb") as f:
                    cache.setex("%s-%s" % (file.replace(".", "_"), mission_id), 60, f.read())
        except Exception as e:
            print e

    try:
        create_script()
        exec_cmd = ""
        if loadtool == "gatling":
            gatling_bin = os.path.join(Config.GATLING_HOME, "bin")

            exec_cmd = "sh {gatling_bin}/gatling.sh -s {user}.{script_name} -rf {report_folder} -on {result_dir_name}".format(
                gatling_bin=gatling_bin, user=user, script_name=script_name, mission_id=mission_id, report_folder=Config.REPORT_FOLDER,
                result_dir_name="report-%s" % mission_id
            )
        elif loadtool == "jmeter":
            if len(agent_list):
                exec_cmd = "sh {jmeter_home}/bin/jmeter.sh -n -t {jmeter_script_folder}/{user}/{script_name}-{mission_id}.jmx -R {agent_list} -l {jmeter_script_folder}/{user}/{script_name}.{mission_id}.jtl -e -o {report_folder}/report-{mission_id}-jmeter".format(
                    debug_detail_folder=Config.DEBUG_DETAIL_FOLDER, jmeter_home=Config.JMETER_HOME, jmeter_script_folder=Config.JMETER_SCRIPT_FOLDER, user=user,
                    script_name=script_name, report_folder=Config.REPORT_FOLDER, mission_id=mission_id,
                    agent_list=",".join(agent_list)
                )
            else:
                exec_cmd = "sh {jmeter_home}/bin/jmeter.sh -n -t {jmeter_script_folder}/{user}/{script_name}-{mission_id}.jmx -l {jmeter_script_folder}/{user}/{script_name}.{mission_id}.jtl -e -o {report_folder}/report-{mission_id}-jmeter".format(
                    debug_detail_folder=Config.DEBUG_DETAIL_FOLDER, jmeter_home=Config.JMETER_HOME, jmeter_script_folder=Config.JMETER_SCRIPT_FOLDER, user=user,
                    script_name=script_name, report_folder=Config.REPORT_FOLDER, mission_id=mission_id
                )

        cache.append("mission_%s_log" % mission_id, exec_cmd)

        try:
            p = pexpect.spawn(exec_cmd, timeout=120)
        except Exception as e:
            cache.set("mission_%s_error" % mission_id, str(e))
            logger.error(str(e))
        while p.isalive():
            p.expect(['\n', pexpect.EOF, pexpect.TIMEOUT])
            info = p.before
            cache.append("mission_%s_log" % mission_id, "<br>" + info)
        else:
            if loadtool == "jmeter":
                save_to_remote(
                    os.path.join(Config.REPORT_FOLDER, "report-%s-jmeter" % mission_id, "content", "js"),
                    mission_id,
                    ["dashboard.js", "graph.js"]
                )
            elif loadtool == "gatling":
                report_dir = get_gatling_report_dir(mission_id)
                source_dir = os.path.join(Config.REPORT_FOLDER, report_dir)
                report_file = os.path.join(Config.REPORT_FOLDER, "report-gatling", "report-%s.tar.gz" % mission_id)
                with open(os.path.join(Config.REPORT_FOLDER, report_dir, "js", "stats.json")) as f:
                    cache.setex("mission_%s_stats" % mission_id, 60, f.read())
                with tarfile.open(report_file, "w:gz") as tar:
                    tar.add(source_dir, arcname=os.path.basename(source_dir))
                Domino.save(report_file, "report-%s.tar.gz" % mission_id)
            cache.setex("mission_%s_finish" % mission_id, 60, 1)
            cache.delete("mission_%s_log" % mission_id)
            send_wechat_notice(mission_id, user)
    except Exception as e:
        logger.error(traceback.format_exc())
    finally:
        return "ok"
