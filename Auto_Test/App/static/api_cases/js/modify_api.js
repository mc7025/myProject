$(document).ready(function () {
    $("#c_btn").click(function () {
        var c_title_list = ["#", "Name", "Type", "Format", "Path", "isPublic"];
        var c_keyList = ["c_name", "c_type", "c_format", "c_path", "c_isPublic"];
        openModal("Cnn List", c_title_list, "c_table", c_keyList, "/CnnModels/");
        $("#c_table").on('click', '.list_tr', function () {
            var cls = $(this).attr("class");
            if (cls == "list_tr alert-success") {
                $(this).removeClass("alert-success");
            } else {
                $(".list_tr").removeClass("alert-success");
                $(this).attr("class", "list_tr alert-success");
            }
            var td = $(this).find("td");
            c_put_name = td.eq(1).text();
            c_put_id = $(this).attr("matt_id")
        });
    });


    $("#d_btn").click(function () {
        var d_title_list = ["#", "Name", "Type", "Size", "Path"];
        var d_keyList = ["d_name", "d_type", "d_size", "d_path"];
        openModal("Data Set List", d_title_list, "d_table", d_keyList, "/DataModels/");
        $("#d_table").on('click', '.list_tr', function () {
            var cls = $(this).attr("class");
            if (cls == "list_tr alert-success") {
                $(this).removeClass("alert-success");
            } else {
                $(".list_tr").removeClass("alert-success");
                $(this).attr("class", "list_tr alert-success");
            }
            var td = $(this).find("td");
            d_put_name = td.eq(1).text();
            d_put_id = $(this).attr("matt_id")
        });
    });


    $("#modal_btn").click(function () {
        $("#myListModal").modal("hide");
        var table_id = $(".modal-body table").attr("id");
        if (table_id == "c_table") {
            $("#c_btn_input").attr("value", c_put_name);
        } else {
            $("#d_btn_input").attr("value", d_put_name);
        }
    });


    $("#yes_btn").click(function () {
        var a_level = $("#a_level").val();
        var a_type = $("#a_type").val();
        var a_modelId = c_put_id;
        var a_dataId = d_put_id;
        var a_description = $("#a_description").val();
        var a_id = $("#api_id").val();
        $.ajax('/ApiCaseModels/', {
            dataType: "json",
            type: "PUT",
            data: {
                "a_id": a_id,
                "a_level": a_level,
                "a_type": a_type,
                "a_modelId": a_modelId,
                "a_dataId": a_dataId,
                "a_description": a_description,
            },
            success: function () {
                window.location.href = "/apicases/";
            },
        });
    });

    $("#a_description").focus(function () {
        var a_level = $("#a_level").val();
        var a_type = $("#a_type").val();
        var c_name = $("#c_btn_input").val();
        var d_name = $("#d_btn_input").val();
        $(this).val(a_level + "-" + a_type + "-" + c_name + "-" + d_name);
    });

    $("#btn").click(function () {
        btnFun();
    });

    blurFun();

    baseLiFun("api_li");
});