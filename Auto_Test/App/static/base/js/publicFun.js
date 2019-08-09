function createList(obj, page, modviews, keyList) {
    $(".new_tr").remove();
    for (var i = 0; i < obj.length; i++) {
        var ele = "";
        ele += "<tr class=\"new_tr\"><td>" + ((page - 1) * 10 + (i + 1)) + "</td>";
        for (var k of keyList) {
            ele += "<td>" + obj[i][k] + "</td>";
        }
        var del_btn = "<td><button data_id="
            + obj[i].id
            + " class=\"btn btn-default btn-xs btn_del\" data-toggle=\"modal\" data-target=\"#myModal\"><a href=\"#\">Delete</a></button></td>";
        var mod_btn = "<td><button class=\"btn btn-default btn-xs\"><a href=" + "/" + modviews + "/" + obj[i].id + ">Modify</a></button></td>";
        ele += del_btn;
        ele += mod_btn;
        $("#cnn_table").append(ele);
    }
}

function pagination(url, create, modviews, keyList) {
    $(".pagination").on("click", ".p_num", function () {
        var page = Number($(this).text());
        $.getJSON(url + '?page=' + page, function (data) {
            var data_set = data['data'];
            create(data_set, page, modviews, keyList)
        });
        $(".p_num").attr("class", "p_num");
        $(this).attr("class", "active p_num");

        var page_after = Number($(".active.p_num").text());
        if (page_after > 1) {
            $("#pre_page").removeAttr("class");
        } else {
            $("#pre_page").attr("class", "disabled");
        }

        if (page_after < page_num) {
            $("#next_page").removeAttr("class");
        } else {
            $("#next_page").attr("class", "disabled");
        }
    });

    $("#pre_page").click(function () {
        var page = Number($(".active.p_num").text());
        if (page > 1) {
            $("#pre_page").removeAttr("class");
            $.getJSON(url + '?page=' + (page - 1), function (data) {
                var data_set = data['data'];
                create(data_set, (page - 1), modviews, keyList)
            });
            $(".p_num").attr("class", "p_num");
            $("#li" + (page - 1)).attr("class", "active p_num");
        }
        var page_after = Number($(".active.p_num").text());
        if (page_after == 1) {
            $("#pre_page").attr("class", "disabled");
        }
        if (page_after < page_num) {
            $("#next_page").removeAttr("class");
        }
    });

    $("#next_page").click(function () {
        var page = Number($(".active.p_num").text());
        if (page < page_num) {
            $("#next_page").removeAttr("class");
            $.getJSON(url + '?page=' + (page + 1), function (data) {
                var data_set = data['data'];
                create(data_set, (page + 1), modviews, keyList);
            });
            $(".p_num").attr("class", "p_num");
            $("#li" + (page + 1)).attr("class", "active p_num");
        }
        var page_after = Number($(".active.p_num").text());
        if (page_after == page_num) {
            $("#next_page").attr("class", "disabled");
        }
        if (page_after > 1) {
            $("#pre_page").removeAttr("class");
        }
    });
}

function checkInput(input_id) {
    var input_val = $("#" + input_id).val();
    if (input_val) {
        $("#helpBlock_" + input_id).remove();
        var input_parent = $("#" + input_id).parent();
        input_parent.attr('class', "form-group has-success");
        $("#" + input_id).attr("aria-describedby", "helpBlock_" + input_id);
        var ele = "<span id=\"helpBlock_" + input_id + "\" class=\"help-block\"></span>";
        input_parent.append(ele);
    } else {
        $("#helpBlock_" + input_id).remove();
        var input_parent = $("#" + input_id).parent();
        input_parent.attr('class', "form-group has-error");
        $("#" + input_id).attr("aria-describedby", "helpBlock_" + input_id);
        var ele = "<span id=\"helpBlock_" + input_id + "\" class=\"help-block\">Invalid Value</span>";
        input_parent.append(ele);
    }
}

function btnFun() {
    var valList = []
    $("input[type='text']").each(function () {
        var val = $(this).val();
        var id = $(this).attr("id");
        valList.push(val);
        checkInput(id);
    });
    if ($.inArray("", valList) < 0) {
        $('#myModal').modal('show');
    }
}

function blurFun() {
    $("input[type='text']").each(function () {
        var id = $(this).attr("id");
        $(this).blur(function () {
            checkInput(id)
        });
    });
}

function baseLiFun(id) {
    $("#base_ul").siblings("li").removeAttr("class");
    $("#" + id).attr("class", "active");
    $("#" + id + " a").attr("href", "#");
}

function drawPageIcon(page_num) {
    for (var i = 1; i < page_num; i++) {
        var ele = "<li id=\"li" + (i + 1) + "\" class=\"p_num\"><a href=\"#\">" + (i + 1) + "</a></li>";
        $("#next_page").before(ele);
    }
    if (page_num > 1) {
        $("#next_page").removeAttr("class");
    }
}

function createListNoBtn(obj, page, keyList, table_id) {
    $(".list_tr").remove();
    for (var i = 0; i < obj.length; i++) {
        var ele = "";
        ele += "<tr class=\"list_tr\" matt_id=\"" + obj[i].id + "\"><td>" + ((page - 1) * 10 + (i + 1)) + "</td>";
        for (var k of keyList) {
            ele += "<td>" + obj[i][k] + "</td>";
        }
        $("#" + table_id).append(ele);
    }
}


function drawTableTitle(titleList, table_id) {
    var table_ele = "<table class=\"table table-condensed\" id=\"" + table_id + "\"><tr>";
    for (var key of titleList) {
        table_ele += "<th>" + key + "</th>";
    }
    table_ele += "</tr></table>";
    $(".modal-body nav").before(table_ele);
}


function openModal(title, title_list, table_id, key_list, url) {
    $(".modal-header h3").text(title);
    $(".modal-body table").remove();
    drawTableTitle(title_list, table_id);
    $.getJSON(url, function (data) {
        var obj = data['data'];
        page_num = data["page_num"];
        createListNoBtn(obj, 1, key_list, table_id);
        drawPageIcon(page_num);
    });
    $(".list_tr").removeClass("alert-success");
    $("#myListModal").modal("show");
}

function taskCreateList(obj, page, modviews) {
    $(".new_tr").remove();
    for (var i = 0; i < obj.length; i++) {
        var ele = "";
        ele += "<tr class=\"new_tr\" hostid=\"" + obj[i].t_hostId + "\" apiId=\"" + obj[i].t_apiCaseId + "\" sampleId=\"" + obj[i].t_sampleCaseId + "\"><td>" + ((page - 1) * 10 + (i + 1)) + "</td>";
        if (obj[i]["t_caseType"] == "Api") {
            var keyList = ["t_caseType", "t_hostIp", "t_apiCase", "t_duration", "t_status", "t_description"];
        } else {
            var keyList = ["t_caseType", "t_hostIp", "t_sampleCase", "t_duration", "t_status", "t_description"];
        }
        for (var k of keyList) {
            ele += "<td>" + obj[i][k] + "</td>";
        }
        var del_btn = "<td><button data_id="
            + obj[i].id
            + " class=\"btn btn-default btn-xs btn_del\"><a href=\"#\">Delete</a></button></td>";
        var mod_btn = "<td><button class=\"btn btn-default btn-xs btn_mod\"><a href=\"#\">Modify</a></button></td>";
        ele += del_btn;
        ele += mod_btn;
        $("#cnn_table").append(ele);
    }
}

function taskPagination(url, create, modviews) {
    $(".pagination").on("click", ".p_num", function () {
        var page = Number($(this).text());
        $.getJSON(url + '?page=' + page, function (data) {
            var data_set = data['data'];
            taskCreateList(data_set, page, modviews);
        });
        $(".p_num").attr("class", "p_num");
        $(this).attr("class", "active p_num");

        var page_after = Number($(".active.p_num").text());
        if (page_after > 1) {
            $("#pre_page").removeAttr("class");
        } else {
            $("#pre_page").attr("class", "disabled");
        }

        if (page_after < page_num) {
            $("#next_page").removeAttr("class");
        } else {
            $("#next_page").attr("class", "disabled");
        }
    });

    $("#pre_page").click(function () {
        var page = Number($(".active.p_num").text());
        if (page > 1) {
            $("#pre_page").removeAttr("class");
            $.getJSON(url + '?page=' + (page - 1), function (data) {
                var data_set = data['data'];
                taskCreateList(data_set, (page - 1), modviews);
            });
            $(".p_num").attr("class", "p_num");
            $("#li" + (page - 1)).attr("class", "active p_num");
        }
        var page_after = Number($(".active.p_num").text());
        if (page_after == 1) {
            $("#pre_page").attr("class", "disabled");
        }
        if (page_after < page_num) {
            $("#next_page").removeAttr("class");
        }
    });

    $("#next_page").click(function () {
        var page = Number($(".active.p_num").text());
        if (page < page_num) {
            $("#next_page").removeAttr("class");
            $.getJSON(url + '?page=' + (page + 1), function (data) {
                var data_set = data['data'];
                taskCreateList(data_set, (page + 1), modviews);
            });
            $(".p_num").attr("class", "p_num");
            $("#li" + (page + 1)).attr("class", "active p_num");
        }
        var page_after = Number($(".active.p_num").text());
        if (page_after == page_num) {
            $("#next_page").attr("class", "disabled");
        }
        if (page_after > 1) {
            $("#pre_page").removeAttr("class");
        }
    });
}

