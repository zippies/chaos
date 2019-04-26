# -*- encoding:utf-8 -*-
from jmeter_report_template import jmeter_report_template_dict
from script_template import jmeter_template, gatling_template

apilist_template = """
<div class="col-md-11 apilistitem apipanel" id="apilistDetail-{{id}}">
    <h5><span class="label label-success">请求设置</span></h5>
    <div style="padding-left:20px">
        <input type="checkbox" name="apiitems" checked="checked" style="display:none"/>
        <ul class="list-inline" style="width:100%">
            <li>接口路径:</li>
            <li>
                <select name="type-{{id}}" class="form-control">
                    <option value="GET">GET</option>
                    <option value="POST">POST</option>
                </select>
            </li>
            <li style="width:60%">
                <input id="path-{{id}}" name="path-{{id}}" class="form-control" maxlength="5000" type="text" placeholder="接口地址" value="{{ test_path }}" onblur="$(this).attr('value', $(this).val())">
            </li>
            <li><a class="btn btn-default" href="javascript:;" onclick="testapi({{id}})">测试一下</a></li>
            <li><a href="javascript:;" class="btn btn-danger" onclick="delapi({{id}})">删除</a></li>
        </ul>
        <ul class="list-inline">
            <li>读取文件:</li>
            <li style="display: none">
                <label class="radio-inline">
                  <input type="radio" name="radio-filetype-{{id}}" value="data" checked="checked" onclick="$('#filefield-{{id}}').hide()"> 请求数据
                </label>
            </li>
            <li style='display: none'>
                <label class="radio-inline">
                  <input type="radio" name="radio-filetype-{{id}}" value="file" onclick="$('#filefield-{{id}}').show()"> 文件上传
                </label>
            </li>
            <li id="filefield-{{id}}" style="display:none"><input type="text" placeholder="表单field" class="form-control" name="filefield-{{id}}"></li>
            <li><input type="file" name="file-{{id}}" class="form-control form-file" accept="txt,csv,tsv"></li>
            {% if helpon %}
            <li><a tabindex="0" href="javascript:;" id="helponfile" role="button" data-toggle="popover" data-trigger="focus" title="适用场景及用法" data-content='{{ helponfile }}'><span class="glyphicon glyphicon-question-sign"></span></a></li>
            {% endif %}
            <li>文件内数据分隔符: </li>
            <li><input type="text" value="," name="delimiter-{{id}}" class="form-control"></li>
        </ul>
        <ul class="nav nav-tabs">
            <li role="presentation" class="active"><a href="#requestbodypanel-{{id}}" aria-controls="requestbodypanel-{{id}}" role="tab" data-toggle="tab">请求体(body)</a></li>
            <li role="presentation"><a href="#requestheaderpanel-{{id}}" aria-controls="requestheaderpanel-{{id}}" role="tab" data-toggle="tab">请求头(header)</a></li>
        </ul>
        <div class="tab-content">
            <!-- body begin -->
            <div role="tabpanel" class="tab-pane active" id="requestbodypanel-{{id}}">
                <div class="panel-body" id="req-body-panel-{{id}}">
                    <textarea id="bodyarea-{{id}}" name="requestbody-{{id}}" class="form-control" style="height:100px" placeholder='{{ placeholder_data }}' onblur="$(this).html($(this).val())">{{ test_data }}</textarea>
                </div>
            </div>
            <div role="tabpanel" class="tab-pane" id="requestheaderpanel-{{id}}">
                <div class="panel-body" id="req-header-panel-{{id}}">
                    <textarea id="headerarea" name="requestheader-{{id}}" class="form-control" placeholder='{{ placeholder_header }}' onblur="$(this).html($(this).val())"></textarea>
                </div>
            </div>
        </div>
    </div>
    <hr>
    <h5><span class="label label-danger">响应断言</span></h5>
    <div style="padding-left:20px">
        <ul class="list-inline">
            <li>响应(code)等于:</li>
            <li><input type="text" name="equal-code-{{id}}" value="200" onblur="$(this).attr('value', $(this).val())"></li>
        </ul>
        <ul class="list-inline">
            <li>响应(body)包含:</li>
            <li>
                <input type="text" name="containValue-body-{{id}}" placeholder="可以使用正则表达式" onblur="$(this).attr('value', $(this).val())">
            </li>
        </ul>
        <ul class="list-inline">
            <li>响应(time)小于 :</li>
            <li>
                <input type="text" name="responseTime-body-{{id}}" placeholder="单位：毫秒" onblur="$(this).attr('value', $(this).val())">
            </li>
        </ul>
        <hr>
        <a href="javascript:;" onclick="addenv({{id}})">添加变量</a>
        {% if helpon %}
        <a tabindex="0" href="javascript:;" id="helponenv" role="button" data-toggle="popover" data-trigger="focus" title="适用场景及用法" data-content='{{ helponenv }}'><span class="glyphicon glyphicon-question-sign"></span></a>
        {% endif %}
        <div id="envlist-{{id}}" style="margin-top:10px;maring-left:10px">
        </div>
        <hr>
        <div style="margin-bottom:10px">
            思考时间：<input type="text" name="thinktime-{{id}}" value="" onblur="$(this).attr('value', $(this).val())"> 秒
        </div>
    </div>
</div>
"""

result_template = """
<div style="margin-left:20px;margin-top:10px">
    <h5>请求数据：</h5>
    <div style="margin-left:20px;margin-top:10px">
        <label>URL:</label> <span class="label label-success">{{ method }}</span>
        <div>
            <div> <pre>{{ url }}</pre></div>
            {% if req_header != "{}" %}
                <div><label>header:</label></div>
                <div><pre>{{ req_header }}</pre></div>
            {% endif %}
            {% if req_body != "{}" %}
                <div><label>body:</label></div>
                <div><pre>{{ req_body }}</pre></div>
            {% endif %}
        </div>
    </div>
    <h5>响应数据：</h5>
    <div style="margin-left:20px;margin-top:10px">
        <label>HttpCode: </label><span class="label label-{% if resp_code == 200 %}success{% else %}danger{% endif %}"> {{ resp_code }}</span>
        {% if resp_code %}<label style="margin-left:20px">ResponseTime: </label> <span class="label label-success"> {{ resp_elapsed }} ms</span>{% endif %}
        <div>
            <label>Header:</label>
        </div>
        <div>
            <textarea class="form-control" style="height:70px">{{ resp_header }}</textarea>
        </div>
        <div>
            <label>body:</label>
        </div>
        <div>
            <textarea class="form-control" style="height:250px">{{ resp_body }}</textarea>
        </div>
    </div>
    {% if envs %}
        <hr>
        <label>保存变量值</label>
        <ul>
        {% for env in envs %}
            <li>{{ env[0] }} = "{{ env[1] }}"</li>
        {% endfor %}
        </ul>
    {% endif %}
</div>
"""

machine_template = """
{% for machine in machines %}
    <div class="col-lg-3 col-md-4 col-sm-6" id="machinediv_{{ machine.id }}" style="margin-bottom:10px">
        <div class="machine" id="machinediv_{{ machine.id }}" style="padding:15px;text-align:center;background-color: #EEC591">
            <table class="table table-bordered" id="machineinfotable">
                <tbody>
                    <tr>
                        <th>名 称</th>
                        <td>
                            <input class="machineinfo_{{ machine.id }} machineinput" name="name" type="text" value="{{ machine.name }}" disabled="disabled">
                        </td>
                    </tr>
                    <tr>
                        <th>HOST</th>
                        <td>
                            <input class="machineinfo_{{ machine.id }} machineinput" name="ip" type="text" value="{{ machine.ip }}" disabled="disabled">
                        </td>
                    </tr>
                    <tr>
                        <th>CPU</th>
                        <td>
                            <input class="machineinfo_{{ machine.id }} machineinput" name="cpu" type="text" value="{{ machine.cpu }}" disabled="disabled">
                        </td>
                    </tr>
                    <tr>
                        <th>内 存</th>
                        <td>
                            <input class="machineinfo_{{ machine.id }} machineinput" name="memory" type="text" value="{{ machine.memory }}" disabled="disabled">
                        </td>
                    </tr>
                    <tr>
                        <th>磁 盘</th>
                        <td>
                            <input class="machineinfo_{{ machine.id }} machineinput" name="disk" type="text" value="{{ machine.disk }}" disabled="disabled">
                        </td>
                    </tr>
                </tbody>
            </table>
            <a href="javascript:;" class="btn btn-info" id="editmachine_{{ machine.id }}" onclick="editmachine({{ machine.id }})" style="width:44%">编辑</a>
            <a href="javascript:;" class="btn btn-info" id="saveedit_{{ machine.id }}" onclick="saveedit({{ machine.id }})" style="display:none;width:44%">保存</a>
            <a href="javascript:;" class="btn btn-warning" id="delmachine_{{ machine.id }}" onclick="delmachine({{ machine.id }})" style="width:44%">删除</a>
        </div>
    </div>
{% endfor %}
"""

monitor_template = """
<div id="monitor-{{ timestamp }}">
<hr>
<ul class="list-inline">
    {% for url in url_list %}
        <li><iframe src="{{ url }}" height="250" frameborder="0"></iframe></li>
    {% endfor %}
</ul>
<span style="margin-left:80px">空间: {{ namespace }}</span> <span style="margin-left:50px">实例: {{ instance_name }}</span> <button class="btn btn-xs btn-danger" onclick="$('#monitor-{{ timestamp }}').remove()" style="margin-left:50px">remove</button>
</div>
"""
