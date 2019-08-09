$(document).ready(function () {
    var keyList = ["c_name", "c_type", "c_format", "c_path", "c_isPublic"];

    $.getJSON('/CnnModels/', function (data) {
        var cnns = data['data'];
        page_num = data["page_num"];
        createList(cnns, 1, "modmodel", keyList);
        drawPageIcon(page_num);
    });

    pagination('/CnnModels/', createList, "modmodel", keyList);

    $("#cnn_table").on("click", ".btn_del", function () {
        dataId = $(this).attr("data_id");
    });

    baseLiFun("cnns_li");

    $("#yes_btn").click(function () {
        $.ajax('/CnnModels/', {
            type: "DELETE",
            data_type: "json",
            data: {
                "c_id": dataId,
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