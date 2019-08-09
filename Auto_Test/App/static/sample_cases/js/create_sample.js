$(document).ready(function () {


    $("#c_cls_btn").click(function () {
        var c_title_list = ["#", "Name", "Type", "Format", "Path", "isPublic"];
        var c_keyList = ["c_name", "c_type", "c_format", "c_path", "c_isPublic"];
        openModal("Cnn List", c_title_list, "c_cls_table", c_keyList, "/CnnModels/");
        $("#c_cls_table").on('click', '.list_tr', function () {
            var cls = $(this).attr("class");
            if (cls == "list_tr alert-success") {
                $(this).removeClass("alert-success");
            } else {
                $(".list_tr").removeClass("alert-success");
                $(this).attr("class", "list_tr alert-success");
            }
            var td = $(this).find("td");
            c_cls_put_name = td.eq(1).text();
            c_cls_put_id = $(this).attr("matt_id")
        });
    });

    $("#c_det_btn").click(function () {
        var c_title_list = ["#", "Name", "Type", "Format", "Path", "isPublic"];
        var c_keyList = ["c_name", "c_type", "c_format", "c_path", "c_isPublic"];
        openModal("Cnn List", c_title_list, "c_det_table", c_keyList, "/CnnModels/");
        $("#c_det_table").on('click', '.list_tr', function () {
            var cls = $(this).attr("class");
            if (cls == "list_tr alert-success") {
                $(this).removeClass("alert-success");
            } else {
                $(".list_tr").removeClass("alert-success");
                $(this).attr("class", "list_tr alert-success");
            }
            var td = $(this).find("td");
            c_det_put_name = td.eq(1).text();
            c_det_put_id = $(this).attr("matt_id")
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
        if (table_id == "c_cls_table") {
            $("#c_cls_btn_input").attr("value", c_cls_put_name);
        }  else if (table_id == "c_det_table") {
            $("#c_det_btn_input").attr("value", c_det_put_name);
        } else if (table_id == "d_table") {
            $("#d_btn_input").attr("value", d_put_name);
        }
    });

    $("#yes_btn").click(function () {
        var s_type = $("#s_type").val();
        var s_modelClsId = c_cls_put_id;
        var s_modelDetId = c_det_put_id;
        var s_dataId = d_put_id;
        var s_description = $("#s_description").val();
        $.post("/SampleCaseModels/", {
            "s_type": s_type,
            "s_modelClsId": s_modelClsId,
            "s_modelDetId": s_modelDetId,
            "s_dataId": s_dataId,
            "s_description": s_description
        }, function () {
            window.location.href = "/samplecases/";
        })
    });

    $("#s_description").focus(function () {
        var s_type = $("#s_type").val();
        var s_modelCls = $("#c_cls_btn_input").val();
        var s_modelDet = $("#c_det_btn_input").val();
        var d_name = $("#d_btn_input").val();
       $(this).val(s_type + "-" + s_modelCls + "-" + s_modelDet + "-" + d_name);
    });

    $("#btn").click(function () {
        btnFun();
    });

    blurFun();

    baseLiFun("sample_li");

});