$(document).ready(function () {
    $("#t_hostIp_btn").click(function () {
        var h_title_list = ["#", "IP", "OS"];
        var h_keyList = ["h_ip", "h_os"];
        openModal("Host List", h_title_list, "host_table", h_keyList, "/HostModels/");
        $("#host_table").on('click', '.list_tr', function () {
            var cls = $(this).attr("class");
            if (cls == "list_tr alert-success") {
                $(this).removeClass("alert-success");
            } else {
                $(".list_tr").removeClass("alert-success");
                $(this).attr("class", "list_tr alert-success");
            }
            var td = $(this).find("td");
            host_put_name = td.eq(1).text();
            host_put_id = $(this).attr("matt_id")
        });
    });

    $("#case_descriptionn_btn").click(function () {
        var t_caseType = $("#t_caseType option:selected").text();
        if (t_caseType == "Api") {
            var api_title_list = ["#", "Level", "Type", "Model", "Data", "Description"];
            var api_keyList = ["a_level", "a_type", "c_name", "d_name", "a_description"];
            openModal("Api Case List", api_title_list, "api_table", api_keyList, "/ApiCaseModels/");
            $("#api_table").on('click', '.list_tr', function () {
                var cls = $(this).attr("class");
                if (cls == "list_tr alert-success") {
                    $(this).removeClass("alert-success");
                } else {
                    $(".list_tr").removeClass("alert-success");
                    $(this).attr("class", "list_tr alert-success");
                }
                var td = $(this).find("td");
                api_put_name = td.eq(5).text();
                api_put_id = $(this).attr("matt_id")
            });
        } else {
            var sample_title_list = ["#", "Type", "Classify Model", "Detect Model", "Data", "Description"];
            var sample_keyList = ["s_type", "s_modelClsName", "s_modelDetName", "s_dataName", "s_description"];
            openModal("Sample Case List", sample_title_list, "sample_table", sample_keyList, "/SampleCaseModels/");
            $("#sample_table").on('click', '.list_tr', function () {
                var cls = $(this).attr("class");
                if (cls == "list_tr alert-success") {
                    $(this).removeClass("alert-success");
                } else {
                    $(".list_tr").removeClass("alert-success");
                    $(this).attr("class", "list_tr alert-success");
                }
                var td = $(this).find("td");
                sample_put_name = td.eq(5).text();
                sample_put_id = $(this).attr("matt_id")
            });
        }
    });

    $("#modal_btn").click(function () {
        $("#myListModal").modal("hide");
        var table_id = $(".modal-body table").attr("id");
        if (table_id == "host_table") {
            $("#t_hostIp_btn_input").attr("value", host_put_name);
        } else if (table_id == "api_table") {
            $("#case_description_btn_input").attr("value", api_put_name);
        } else if (table_id == "sample_table") {
            $("#case_description_btn_input").attr("value", sample_put_name);
        }
    });

    $("#yes_btn").click(function () {
        var t_caseType = $("#t_caseType option:selected").text();
        var t_hostId = host_put_id;
        if (t_caseType == "Api") {
            var t_apiCaseId = api_put_id;
            var t_sampleCaseId = "False";
        } else {
            var t_apiCaseId = "False";
            var t_sampleCaseId = sample_put_id;
        }
        var t_duration = $("#t_duration").val();
        var t_description = $("#t_description").val();
        var t_id = $("#t_id").val();
        $.ajax('/TaskModels/', {
            dataType: "json",
            type: "PUT",
            data: {
                "t_id": t_id,
                "t_caseType": t_caseType,
                "t_hostId": t_hostId,
                "t_apiCaseId": t_apiCaseId,
                "t_sampleCaseId": t_sampleCaseId,
                "t_duration": t_duration,
                "t_description": t_description,
            },
            success: function () {
                window.location.href = "/tasks/";
            },
        });
    });

    $("#t_description").focus(function () {
        // var t_caseType = $("#t_caseType option:selected").text();
        var t_hostIp = $("#t_hostIp_btn_input").val();
        var case_description = $("#case_description_btn_input").val();
        var t_duration = $("#t_duration").val();
        $(this).val(t_hostIp + "-" + case_description + "-" + t_duration);
    });

    $("#btn").click(function () {
        btnFun();
        $("#selectDiv").attr("class", "form-group has-success");
    });

    blurFun();

    baseLiFun("task_li");
});