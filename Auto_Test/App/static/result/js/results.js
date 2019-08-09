$(document).ready(function () {
    function createResultList(obj, page, result, keyList) {
        $(".new_tr").remove();
        for (var i = 0; i < obj.length; i++) {
            var ele = "";
            ele += "<tr class=\"new_tr\"><td>" + ((page - 1) * 10 + (i + 1)) + "</td>";
            for (var k of keyList) {
                ele += "<td>" + obj[i][k] + "</td>";
            }
            var detail_btn = "<td><button class=\"btn btn-default btn-xs\"><a href=" + "/" + result + "/" + obj[i].id + ">Detail</a></button></td>";
            ele += detail_btn;
            $("#cnn_table").append(ele);
        }
    }

    var keyList = ["r_taskName", "r_result"];

    $.getJSON('/ResultModels/', function (data) {
        var results = data['data'];
        page_num = data["page_num"];
        createResultList(results, 1, "result", keyList);
        drawPageIcon(page_num);
    });

    pagination('/ResultModels/', createResultList, "result", keyList);

    baseLiFun("result_li");

});