$(document).ready(function () {
    var keyList = ["a_level", "a_type", "c_name", "d_name", "a_description"];

    $.getJSON('/ApiCaseModels/', function (data) {
        var apis = data['data'];
        page_num = data["page_num"];
        createList(apis, 1, "modapi", keyList);
        drawPageIcon(page_num);
    });

    pagination('/ApiCaseModels/', createList, "modapi", keyList);

    $("#cnn_table").on("click", ".btn_del", function () {
        dataId = $(this).attr("data_id");
    });

    baseLiFun("api_li");

    $("#yes_btn").click(function () {
        $.ajax('/ApiCaseModels/', {
            type: "DELETE",
            data_type: "json",
            data: {
                "a_id": dataId,
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