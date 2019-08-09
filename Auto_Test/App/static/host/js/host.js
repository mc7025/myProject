$(document).ready(function () {
    var keyList = ["h_ip", "h_os"];

    $.getJSON('/HostModels/', function (data) {
        var hosts = data['data'];
        page_num = data["page_num"];
        createList(hosts, 1, "modhost", keyList);
        drawPageIcon(page_num);
    });

    pagination('/HostModels/', createList, "modhost", keyList);

    $("#cnn_table").on("click", ".btn_del", function () {
        dataId = $(this).attr("data_id");
    });

    baseLiFun("hosts_li");

    $("#yes_btn").click(function () {
        $.ajax('/HostModels/', {
            type: "DELETE",
            data_type: "json",
            data: {
                "h_id": dataId,
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