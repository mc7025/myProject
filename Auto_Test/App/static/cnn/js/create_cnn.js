$(document).ready(function () {
    $("#yes_btn").click(function () {
        var c_name = $("#model_name").val();
        var c_type = $("#model_type").val();
        var c_format = $("#model_format").val();
        var c_path = $("#model_path").val();
        var c_isPublic = $("input[name='inlineRadioOptions']:checked").val();
        $.post("/CnnModels/", {
            "c_name": c_name,
            "c_type": c_type,
            "c_format": c_format,
            "c_path": c_path,
            "c_isPublic": c_isPublic,
        }, function () {
            window.location.href = "/cnns/";
        })
    });

    $("#btn").click(function () {
        btnFun();
    });

    blurFun();

    baseLiFun("cnns_li");
});