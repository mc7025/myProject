$(document).ready(function () {
    $("#yes_btn").click(function () {
        var d_name = $("#data_name").val();
        var d_type = $("#data_type option:selected").text();
        var d_size = $("#data_size").val();
        var d_path = $("#data_path").val();
        $.post("/DataModels/", {
            "d_name": d_name,
            "d_type": d_type,
            "d_size": d_size,
            "d_path": d_path,
        }, function () {
            window.location.href = "/dataset/";
        })
    });

    $("#btn").click(function () {
        btnFun();
        $("#selectDiv").attr("class", "form-group has-success");
    });

    blurFun();

    $("#data_type").change(function () {
        var d_type = $("#data_type option:selected").text();
        if (d_type == "Video") {
            $('#data_size').attr("readonly", "readonly");
            $('#data_size').attr("value", "None");
        } else {
            $("#data_size").removeAttr("readonly", "readonly");
            $('#data_size').attr("placeholder", "Data Size");
        }
    });

    baseLiFun("dataset_li");
});