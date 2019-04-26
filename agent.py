# -*- encoding:utf-8 -*-
from app.services.agentService import Agent
from lib.logger import get_logger
from kombu import Exchange, Queue
from configer import agent_tag, redis_host, redis_port, agent_broker_db, agent_backend_db, master_host_port
from celery import Celery
import traceback
import time
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

celery_agent = Celery(
    "chaos-jmeter-agent-worker",
    broker="redis://{host}:{port}/{db}".format(host=redis_host, port=redis_port, db=agent_broker_db),
    backend="redis://{host}:{port}/{db}".format(host=redis_host, port=redis_port, db=agent_backend_db)
)
celery_agent.conf.CELERY_TIMEZONE = 'UTC'

queue = set()
route = dict()

queue.add(Queue(agent_tag, Exchange("Exchange", type="direct"), routing_key="%s_key" % agent_tag))
route["agent.%s" % agent_tag] = {"queue": agent_tag, "routing_key": "%ss_key" % agent_tag}

celery_agent.conf.update(CELERY_QUEUES=queue, CELERY_ROUTES=route)


celery_func_string = """
@celery_agent.task
def {func_name}():
    timenow = time.strftime("%Y-%m-%d %H:%M:%S")
    logger = get_logger(timenow, "INFO", "logs/agent.log")
    agent = Agent()
    agent.start()
    while agent.is_alive():
        logger.info("report to: [%s]" % master_host_port)
        try:
            agent.report_status()
        except Exception as e:
            logger.error(traceback.format_exc())
        time.sleep(2)
    else:
        logger.info("agent exist")
""".format(func_name=agent_tag)

exec(celery_func_string)
