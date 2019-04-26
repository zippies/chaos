# encoding:utf-8
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from app.services.cacheService import get_all_missions, get_all_results
from tasks import worker_run_job
from configer import activate
from threading import Thread
from configer import Config
from StringIO import StringIO
from app import logger, flask_cache
import os, traceback


class Horner(Thread):
    def __init__(self, missionid, missionName, script, username, loadtool, agents):
        Thread.__init__(self)
        self.missionid = missionid
        self.missionName = missionName
        self.script = script
        self.username = username
        self.job_id = None
        self.loadtool = loadtool
        self.agents = agents

    def _analysis_result(self, result):
        try:
            flask_cache.delete("all_results")
            get_all_results()
            flask_cache.delete("all_missions")
            get_all_missions()
        except Exception as e:
            logger.info("cache updated")
        logger.info("[%s]finish callback" % result.id)

    def run(self):
        job = worker_run_job.apply_async(args=[self.loadtool, self.username, self.missionName, self.script, self.missionid, self.agents], queue=activate)
        job.then(self._analysis_result)
        logger.info("任务id:" + job.id)
        self.job_id = job.id


class Monitor(SSHClient):
    def __init__(self, name, missionid, host, port, username, frequency=1, count=30, password=None, pkeycontent=None,
                 **kwargs):
        SSHClient.__init__(self)
        self.name = name
        self.missionid = missionid
        self.frequency = frequency
        self.count = count
        self.homedir = "/home/%s" % username if username != "root" else "/root"
        self.set_missing_host_key_policy(AutoAddPolicy())
        key = StringIO(pkeycontent)
        pkey = RSAKey.from_private_key(key) if pkeycontent else None
        self.connect(hostname=host, port=port, username=username, password=password, pkey=pkey, **kwargs)
        self.sftpclient = self.open_sftp()

    def pushFile(self):
        """将监控工具nmon传输到被测机器上"""
        passed = True
        errorMsg = None
        localfile = Config.nmon_file_path
        remotefile = "%s/nmon" % self.homedir
        logger.info("localfile: %s" % localfile)
        logger.info("remotefile: %s" % remotefile)

        try:
            logger.info("pkill -f nmon")
            stdin, stdout, stderr = self.exec_command("pkill -f nmon")
            logger.info("pushFile 'nmon' to remote machine..")
            self.sftpclient.put(localfile, remotefile, confirm=True)
            logger.info("success!")
        except Exception as e:
            errorMsg = "pushFile Failed:%s" % str(e)
            logger.error(traceback.format_exc())
            passed = False
        finally:
            return passed, errorMsg

    def startMonitor(self):
        """远程启动被测机器上的nmon，生成监控数据"""
        stdin, stdout, stderr = self.exec_command("/usr/sbin/lsof|grep  nmon|awk '{print $2}'|xargs kill -9")
        logger.info("kill -9 执行输出:" + stderr.read() + stdout.read())
        stdin, stdout, stderr = self.exec_command(
            "export TERM=xterm&chmod a+x nmon&export NMON=dmn&./nmon -F %s_%s.nmon -t -s %s -c %s" % (
                self.name, self.missionid, self.frequency, self.count
            )
        )
        error_info = stderr.read()
        if error_info:
            logger.error(error_info + stdout.read())

    @property
    def isready(self):
        """检查被测机器上的nmon监控线程是否结束"""
        stdin, stdout, stderr = self.exec_command("pgrep -lf nmon")
        info = stdout.read().strip()
        if not info:
            return True
        else:
            return False

    def getResult(self):
        """从远程机器上将nmon运行结果文件保存到本地，并使用nmonchart工具生成性能报告，保存到Config.machine_report_dir"""
        success = True
        errorMsg = None
        remote_file = "%s/%s_%s.nmon" % (self.homedir, self.name, self.missionid)
        local_file = "%s/%s_%s.nmon" % (Config.nmon_file_dir, self.name, self.missionid)
        report_file = "%s/%s_%s.html" % (Config.machine_report_dir, self.name, self.missionid)

        cmd = "%s/./nmonchart %s %s" % (Config.bin_path, local_file, report_file)
        logger.info("[cmd]generate nmon report: %s" % cmd)

        try:
            self.sftpclient.get(remote_file, local_file)
            os.system(cmd)
        except Exception as e:
            logger.error(traceback.format_exc())
            success = False
            errorMsg = str(e)
        finally:
            try:
                self.close()
            except:
                pass
            return success, errorMsg, "%s_%s.html" % (self.name, self.missionid)
