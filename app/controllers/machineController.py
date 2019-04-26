# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify
from app.models import db, Machine
from flask_login import login_required, current_user
from jinja2 import Template
from configer import open_admin
from app.controllers import url
from app import logger
from code_templates import machine_template
from StringIO import StringIO
import paramiko, traceback


@url.route("/machines")
@login_required
def machines():
    machines = Machine.query.filter_by(username=current_user.nickname).all()
    return render_template("machines.html", choiced="machines", machines=machines, isadmin=open_admin, nickname=current_user.nickname)


@url.route("/machines/admin")
@login_required
def machines_admin():
    machines = Machine.query.all()
    return render_template("machines.html", choiced="machines", machines=machines, isadmin=True)


@url.route("/getmachines")
@login_required
def getMachines():
    isadmin = eval(request.args.get("isadmin"))
    machines = None
    if isadmin:
        machines = Machine.query.all()
    else:
        machines = Machine.query.filter_by(username=current_user.nickname).all()
    data = Template(machine_template).render(
        machines=machines
    )
    return data


@url.route("/newmachine", methods=["POST"])
@login_required
def newMachine():
    info = {"result": True, "errorMsg": None}
    rsacontent = request.form.get("privatekey")
    ip = request.form.get("ip").strip()
    user = request.form.get("user")
    password = request.form.get("password")
    sshtype = request.form.get("sshtype")
    port = int(request.form.get("port")) or 22

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if sshtype == "password":
            logger.info("ip: %s port: %s user: %s password: %s" % (ip, port, user, password))
            ssh.connect(hostname=ip, port=port, username=user, password=password, timeout=10)
        elif sshtype == "privatekey":
            key = StringIO(rsacontent)
            pkey = paramiko.RSAKey.from_private_key(key)
            ssh.connect(hostname=ip, port=port, username=user, pkey=pkey, timeout=10)
        else:
            info["result"] = False
            info["errorMsg"] = "unsupport sshtype"
            return jsonify(info)

        stdin, stdout, stderr = ssh.exec_command("whoami")
        if user != stdout.readline().strip():
            info["result"] = False
            info["errorMsg"] = stderr.read().decode()
            return jsonify(info)

        cmd_disk = "df -m"
        stdin, stdout, stderr = ssh.exec_command(cmd_disk)

        diskinfos = stdout.readlines()
        diskinfo = diskinfos[1] if "%" in diskinfos[1] else diskinfos[2]
        disk = [i.strip() for i in diskinfo.split(" ") if i.strip()][1]

        cmd_mem = "free -m"
        stdin, stdout, stderr = ssh.exec_command(cmd_mem)
        mem = [i.strip() for i in stdout.readlines()[1].split(" ") if i.strip()][1]

        cmd_cpu = "cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c"
        stdin, stdout, stderr = ssh.exec_command(cmd_cpu)
        cpu = stdout.read().strip()

        logger.info("disk: %s memory: %s cpu: %s" % (disk, mem, cpu))
        ssh.close()

        machine = Machine(
            request.form.get("name"),
            ip=ip,
            sshtype=sshtype,
            user=user,
            port=port,
            password=password,
            rsa=rsacontent,
            memory="%sM" % mem,
            cpu=cpu,
            disk="%sM" % disk,
            username=current_user.nickname
        )
        db.session.add(machine)
        db.session.commit()
        db.session.close()
    except Exception as e:
        logger.error(traceback.format_exc())
        info["result"] = False
        info["errorMsg"] = str(e)
    finally:
        return jsonify(info)


@url.route("/editmachine")
@login_required
def editMachine():
    info = {"result": True, "errorMsg": None}
    req = request.args
    id = int(req.get("id"))
    try:
        machine = Machine.query.filter_by(id=id).first()
        if machine:
            machine.name = req.get("name")
            machine.ip = req.get("ip")
            machine.cpu = req.get("cpu")
            machine.memory = req.get("memory")
            machine.disk = req.get("disk")
            db.session.add(machine)
            db.session.commit()
            db.session.close()
        else:
            info["result"] = False
            info["errorMsg"] = "机器不存在或已被删除"
    except Exception as e:
        info["result"] = False
        info["errorMsg"] = str(e)
    finally:
        return jsonify(info)


@url.route("/delmachine/<int:id>")
@login_required
def delMachine(id):
    info = {"result": True, "errorMsg": None}
    try:
        machine = Machine.query.filter_by(id=id).first()
        if machine:
            db.session.delete(machine)
            db.session.commit()
            db.session.close()
    except Exception as e:
        info["result"] = False
        info["errorMsg"] = str(e)
    finally:
        return jsonify(info)
