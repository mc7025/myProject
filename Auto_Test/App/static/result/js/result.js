$(function () {
    var id = $("#r_id").val();
    $.getJSON('/ResultModels/?r_id=' + id, function (data) {
        var result = data["data"];
        var r_taskName = result[0]["r_taskName"];
        var r_result = result[0]["r_result"];
        var r_errorLog = result[0]["r_errorLog"];
        $("#r_name").val(r_taskName);
        $("#r_result").val(r_result);
        $("#r_errorLog").val(r_errorLog);
    });

    baseLiFun("result_li");
});