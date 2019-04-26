function stop(mission_id, job_id) {
    var index = layer.load(2, {
        shade: [0.1, '#ffa243'],
        offset: '200px'
    });
    $.ajax({
        url: "/stop/" + mission_id + "/" + job_id,
        type: "get",
        error: function (request) {
            layer.msg(request.status, {offset: "100px"});
            layer.close(index);
        },
        success: function (data) {
            layer.close(index);
            if (data.result) {
                layer.msg("停止成功！", {offset: "100px"});
                clearInterval(sessionStorage.current_interval);
                $("#stopbtn").hide();
                $("#startbtn").show();
                $("#monitorMachine").hide();
            } else {
                layer.msg("停止失败:" + data.errorMsg, {offset: "100px"})
            }
        }
    })
}
