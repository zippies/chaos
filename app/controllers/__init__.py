# -*- coding: utf-8 -*-
from flask import Blueprint

url = Blueprint('main', __name__)

from . import missionController, machineController, \
    monitorController, localController, \
    analysisController, agentController
