$(document).ready(function () {
    var keyList = ["d_name", "d_type", "d_size", "d_path"];

    $.getJSON('/DataModels/', function (data) {
        var data_set = data['data'];
        page_num = data["page_num"];
        createList(data_set, 1, "moddataset", keyList);
        drawPageIcon(page_num);
    });

    pagination('/DataModels/', createList, "moddataset", keyList);

    $("#cnn_table").on("click", ".btn_del", function () {
        dataId = $(this).attr("data_id");
    });

    $("#yes_btn").click(function () {
        $.ajax('/DataModels/', {
            type: "DELETE",
            data_type: "json",
            data: {
                "d_id": dataId,
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

    baseLiFun("dataset_li");
});