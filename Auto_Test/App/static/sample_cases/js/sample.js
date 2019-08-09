$(document).ready(function () {
    var keyList = ["s_type", "s_modelClsName", "s_modelDetName", "s_dataName", "s_description"];

    $.getJSON('/SampleCaseModels/', function (data) {
        var samples = data['data'];
        page_num = data["page_num"];
        createList(samples, 1, "modsample", keyList);
        drawPageIcon(page_num);
    });

    pagination('/SampleCaseModels/', createList, "modsample", keyList);

    $("#cnn_table").on("click", ".btn_del", function () {
        dataId = $(this).attr("data_id");
    });

    baseLiFun("sample_li");

    $("#yes_btn").click(function () {
        $.ajax('/SampleCaseModels/', {
            type: "DELETE",
            data_type: "json",
            data: {
                "s_id": dataId,
            },
            success: function (data) {
                if (data["msg"] == "ok") {
                    window.location.reload();
                } else {
                    $("#myModal").modal("hide");
                    $("#prompt").text(data["msg"]);
                    $("#prompt_modal").modal("show");
                }
            },
        });
    });

});