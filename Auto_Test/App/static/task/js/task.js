$(document).ready(function () {
    $.getJSON('/TaskModels/', function (data) {
        var tasks = data['data'];
        page_num = data["page_num"];
        taskCreateList(tasks, 1, "modtask");
        drawPageIcon(page_num);
    });

    taskPagination('/TaskModels/', taskCreateList, "modtask");

    $("#cnn_table").on("click", ".btn_del", function () {
        dataId = $(this).attr("data_id");
        var tr = $(this).parents("tr");
        var td = tr.find("td");
        var status = td.eq(5).text();
        if (status == "Running") {
            $("#prompt").text("This task is running now. Can not delete it.");
            $("#prompt_modal").modal("show");
        }else{
            $("#myModal").modal("show");
        }
    });

    $("#cnn_table").on("click", ".btn_mod", function () {
        var tr = $(this).parents("tr");
        var td = tr.find("td");
        var status = td.eq(5).text();
        if (status == "Running") {
            $("#prompt").text("This task is running now. Can not modify it.");
            $("#prompt_modal").modal("show");
        }else{
            var button = td.eq(7).find("button");
            var dataId = button.attr("data_id");
            console.log(dataId);
            var a = $(this).find("a");
            a.attr("href", "/modtask/" + dataId)
        }
    });

    $("#cnn_table").on("click", ".new_tr", function () {
        var cls = $(this).attr("class");
        if (cls == "new_tr alert-danger") {
            $(this).removeClass("alert-danger");
        } else {
            $(".new_tr").removeClass("alert-danger");
            $(this).attr("class", "new_tr alert-danger");
        }
    });

    $("#run_btn").click(function () {
        var ele = $(".alert-danger");
        if (ele.length == 0) {
            $("#prompt").text("Please choose the task to run.");
            $("#prompt_modal").modal("show");
        } else {
            var td = ele.find("td");
            var status = td.eq(5).text();
            if (status == "Running") {
                $("#prompt").text("The task running now!");
                $("#prompt_modal").modal("show");
            } else {
                var hostid = ele.attr('hostid');
                var type = td.eq(1).text();
                if (type == 'Api') {
                    var apiCaseId = ele.attr('apiid');
                    var sampleCaseId = "False";
                }else{
                    var apiCaseId = "False";
                    var sampleCaseId = ele.attr('sampleid');
                }
                var id = td.eq(7).find("button").attr("data_id");
                $.ajax('/TaskModels/', {
                    dataType: "json",
                    type: "PUT",
                    data: {
                        "r_id": id,
                        "hostid": hostid,
                        "apiCaseId": apiCaseId,
                        "sampleCaseId": sampleCaseId,
                    },
                    success: function (data) {
                        $("#prompt").text(data["msg"]);
                        $("#prompt_modal").modal("show");
                        $("#prompt_modal").on("hidden.bs.modal", function () {
                            window.location.href = "/tasks/";
                        });
                    },
                });
            }
        }
    });

    baseLiFun("task_li");

    $("#yes_btn").click(function () {
        $.ajax('/TaskModels/', {
            type: "DELETE",
            data_type: "json",
            data: {
                "t_id": dataId,
            },
            success: function () {
                window.location.reload();
            },
        });
    });
    
    $("#result_btn").click(function () {
        var ele = $(".alert-danger");
        if (ele.length == 0) {
            $("#prompt").text("Please choose the task to get result.");
            $("#prompt_modal").modal("show");
        } else {
            var td = ele.find("td");
            var status = td.eq(5).text();
            if (status == "Done") {
                var id = td.eq(7).find("button").attr("data_id");
                var a = $(this).find("a");
                a.attr("href", "/result/" + id);
            }else{
                $("#prompt").text("This task is not finished.");
                $("#prompt_modal").modal("show");
            }
        }
    });

});