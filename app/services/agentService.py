# -*- encoding:utf-8 -*-
from app.services.commonService import get_host_ip
from threading import Thread
from configer import master_host_port, Config, agent_tag
from app import cache, logger
import pexpect
import traceback
import requests
import psutil
import json
import time
import os

requests.adapters.DEFAULT_RETRIES = 5

class Agent(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.host = get_host_ip()
        self.session = requests.session()
        self.session.keep_alive = False
        self.starttime = "-"

    def __repr__(self):
        return "[Agent]: %s" % self.name

    def report_status(self):
        url = "http://{host_port}/agent/report/{host}".format(host_port=master_host_port, host=self.host)
        params = {
            "cpu": self._get_cpu(),
            "memory": self._get_memory(),
            "disk": self._get_disk(),
            "tag": agent_tag,
            "starttime": self.starttime
        }
        self.session.get(url, params=params, timeout=(2, 5))

    def _get_cpu(self):
        return "%s%%" % (100 - float(psutil.cpu_percent(1)))

    def _get_memory(self):
        phymem = psutil.virtual_memory()
        line = "%s%%" % (100 - float(phymem.percent))
        return line

    def _get_disk(self):
        disk = os.statvfs('/')
        used = disk.f_blocks - disk.f_bfree
        total = disk.f_blocks - disk.f_bfree + disk.f_bavail
        percent = round(float(used) * 100 / total, 1)
        line = "%s%%" % (100 - percent)
        return line

    def run(self):
        cmd = "sh {jmeter_home}/bin/jmeter-server".format(jmeter_home=Config.JMETER_HOME)
        logger.info(cmd)
        try:
            p = pexpect.spawn(cmd, timeout=120)
            self.starttime = time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            logger.error(traceback.format_exc())

        while p.isalive():
            p.expect(['\n', pexpect.EOF, pexpect.TIMEOUT])
            info = p.before
            logger.info(info)
        else:
            logger.info("[end]")


def get_active_agents():
    return json.loads(cache.get("agents") or "[]")
