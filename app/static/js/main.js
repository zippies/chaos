function get_log() {
    $.ajax({
        url: "/jobdetail/" + sessionStorage.current_mission_id + "/" + $("#debug").get(0).checked,
        type: "get",
        error: function (req) {
            layer.msg(req.status, {offset: "100px"})
        },
        success: function (data) {
            if (data.result) {
                if(data.data){
                    $("#log-detail-div").html(data.data);
                }
                if(data.details){
                    detailstr = "";
                    for(var i in data.details){
                        detailstr += " <a href='" + data.details[i] + "' target='_blank'>"+ i +"</a>";
                    }
                    $("#debugdetail").html(detailstr);
                }
                if (sessionStorage.autobottom === "open") {
                    document.getElementById('bottom').scrollIntoView();
                }
                if (data.finish) {
                    $("#log-detail-div").append("hia~hia~ " + " 运行完成 " + "hia~hia~");
                    clearInterval(sessionStorage.current_interval);
                    $("#startbtn").toggle();
                    $("#stopbtn").toggle();
                    $("#report_url").attr("href", "/report/" + sessionStorage.current_mission_id);
                }
            } else {
                layer.msg("获取日志失败！", {offset: "100px"})
            }
        }
    })
}


function toggleBottom() {
    if (sessionStorage.autobottom === "open") {
        sessionStorage.autobottom = "close";
        layer.msg("关闭底部定位", {offset: "100px"})
    } else {
        sessionStorage.autobottom = "open";
        layer.msg("开启底部定位", {offset: "100px"})
    }
}


function addenv(apiid) {
    if (eval("sessionStorage.envcount_" + apiid + "")) {
        eval("sessionStorage.envcount_" + apiid + " = parseInt(sessionStorage.envcount_" + apiid + ") + 1")
    } else {
        eval("sessionStorage.envcount_" + apiid + " = 1")
    }
    envid = eval("sessionStorage.envcount_" + apiid + "");

    $("#envlist-" + apiid).append("<div id='env-" + apiid + "-" + envid + "'><input type='checkbox' name='env-" + apiid + "' style='display:none' checked='checked'><input type='text' class='required' name='envname-" + apiid + "-" + envid + "' placeholder='变量名' onblur=\"$(this).attr('value', $(this).val())\"> 使用<select name='envextracttype-"+ apiid + "-"+ envid +"'><option value='jsonpath'>JsonPath</option><option value='regex'>正则表达式</option></select>取值自: <label><input type='radio' name='envsource-" + apiid + "-" + envid + "' value='header'> 响应头</label> <label><input type='radio' name='envsource-" + apiid + "-" + envid + "' value='body' checked='checked'> 响应体</label> <input type='text' placeholder='提取表达式'  class='required' name='envexpression-" + apiid + "-" + envid + "' onblur=\"$(this).attr('value', $(this).val())\"> <a href='javascript:;' onclick='delenv(" + apiid + "," + envid + ")'>删除</a></div>")
}


function delenv(apiid, envid) {
    $("#env-" + apiid + "-" + envid).remove()
    eval("sessionStorage.envcount_" + apiid + " = parseInt(sessionStorage.envcount_" + apiid + ") - 1")
}


function testapi(apiid) {
    if (!$.trim($("#baseUrl").val())) {
        $("#baseUrl").focus();
        layer.msg("基础路径不能为空", {offset: "200px"});
        return false;
    }
    if (!$.trim($("#path-" + apiid).val())) {
        $("#path-" + apiid).focus();
        layer.msg("路径不能为空", {offset: "200px"});
        return false;
    }
    layer.load(2, {offset: "400px"});

    var formdata = new FormData($("#addmissionform")[0]);

    $.ajax({
        url: "/testapi/" + apiid,
        type: "POST",
        data: formdata,
        dataType: "JSON",
        cache: false,
        processData: false,
        contentType: false,
        error: function (request) {
            layer.msg(request.status);
            layer.closeAll('loading');
        },
        success: function (data) {
            layer.closeAll('loading');
            if (data.result) {
                layer.open({
                    type: 1,
                    shadeClose: true,
                    title: "测试结果(可按esc键关闭窗口)",
                    shade: false,
                    maxmin: true, //开启最大化最小化按钮
                    area: [document.body.clientWidth, document.body.clientHeight],
                    offset: "0px",
                    content: data.message
                });
            } else {
                layer.msg("运行失败:" + data.errorMsg, {offset: "200px"})
            }
        }
    })
}


function validateForm() {
    var allpass = true;

    for (var i = 1; i <= parseInt(sessionStorage.apicount); i++) {
        if (!$.trim($("#path-" + i).val())) {
            $("#apilist-" + i).click();
            $("#path-" + i).focus();
            layer.msg("path不能为空", {offset: "200px"});
            return false;
        }
    };

    $(".required").each(function() {
        if (!$(this).val()) {
            $(this).focus();
            layer.msg("该值不能为空", {offset: "200px"});
            allpass = false;
        }
    });

    supportType = ["txt", "tsv", "csv"];
    $(".form-file").each(function() {
        filename = $(this).val();
        console.log(filename);
        if(filename){
            fileType = filename.split(".").pop();
            try{
                supportType.indexOf(fileType)
            }catch(error){
                allpass = false;
                layer.msg("文件格式仅支持txt/tsv/csv", {offset: "200px"})
            }
        }
    });

    return allpass
}


function addApi() {
    layer.load(2, {offset: "400px"});
    $("#apilist > a").removeClass("active");
    sessionStorage.apicount = parseInt(sessionStorage.apicount) + 1;
    $("#apilist").append('<a href="javascript:;" id="apilist-' + sessionStorage.apicount +
        '" class="list-group-item active" onclick="showapiconfig(' + sessionStorage.apicount + ')">接口_' +
        sessionStorage.apicount + '</a>');
    $.ajax({
        url: "/getapitemplate/" + sessionStorage.apicount,
        type: "get",
        error: function (request) {
            layer.msg(request.status);
            layer.closeAll('loading');
        },
        success: function (data) {
            $(".apilistitem").hide();
            $("#apilistdiv").append(data);
            layer.closeAll('loading');
        }
    })
}


function showapiconfig(apiid) {
    $("#apilist > a").removeClass("active");
    $("#apilist-" + apiid).addClass("active");
    $(".apilistitem").hide();
    $("#apilistDetail-" + apiid).show()
}


function delapi(apiid) {
    if (parseInt(sessionStorage.apicount) === 1) {
        layer.msg("至少需要保留一个接口", {offset: "200px"});
        return
    }
    $("#apilist-" + apiid).remove();
    $("#apilistDetail-" + apiid).remove();
    sessionStorage.apicount = parseInt(sessionStorage.apicount) - 1;
    $("#apilist-1").click()
}


function switchDispatch() {
    $("#dispatch-item").toggle();
    $("#loop-li").toggle();
}


function changeRadio(element, ctype) {
    $("." + ctype).removeAttr("checked");
    $(element).attr("checked", "checked");
}


function switchLoopType(){
    $(".looptype option").removeAttr("selected");
    selected = $(".looptype").val();
    $(".looptype > option[value='"+ selected +"']").attr("selected", "selected")
}


function choiceMachine(ele){
    if($(ele).attr("checked") === "checked"){
        $(ele).removeAttr("checked")
    }else{
        $(ele).attr("checked", "checked")
    }
}


function input_concurrent(ele){
    $(ele).attr('value', $(ele).val());
    $.ajax({
        url: "/agent/list?concurrent=" + $(ele).val(),
        success: function(data){
            if(data.enable_distributed){
                $("#agent_desc").show();
                $("#agent_list").html(data.agents.length)
            }else{
                $("#agent_desc").hide()
            }
        }
    });
}