$(function () {
    function getData() {
        $.getJSON("/data/", function (datas) {
            var data = datas["data"];
            var throughput = datas["throughput"];
            var myx_power = datas["myx_power"];
            var main_power = datas["main_power"];
            var temp = datas["temp"];
            var efficiency = datas["efficiency"];
            var top1_accuracy = datas["top1_accuracy"];
            var top5_accuracy = datas["top5_accuracy"];
            var span = $("#pf_btn span:eq(0)");
            $("#throughput").text(throughput);
            if (span.text() == "CPU" || span.text() == "GPU") {
                $("#board").text("NULL");
                $("#myx").text("NULL");
                $("#efficiency").text("NULL");
                $("#temp").text("NULL");
            } else {
                $("#board").text(main_power);
                $("#myx").text(myx_power);
                $("#efficiency").text(efficiency);
                $("#temp").text(temp);
            }
            $("#top1").text(top1_accuracy);
            $("#top5").text(top5_accuracy);
            for (var i = 0; i < data.length; i++) {
                var img = data[i]["image"];
                var title = data[i]["title"];
                var span = $("#network_btn span:eq(0)");
                if (span.text() == "VGG_16") {
                    var top1res = (data[i]["top5res"][0] / 100).toFixed(2);
                    var top2res = (data[i]["top5res"][1] / 100).toFixed(2);
                    var top3res = (data[i]["top5res"][2] / 100).toFixed(2);
                    var top4res = (data[i]["top5res"][3] / 100).toFixed(2);
                    var top5res = (data[i]["top5res"][4] / 100).toFixed(2);
                } else {
                    var top1res = data[i]["top5res"][0];
                    var top2res = data[i]["top5res"][1];
                    var top3res = data[i]["top5res"][2];
                    var top4res = data[i]["top5res"][3];
                    var top5res = data[i]["top5res"][4];
                }
                var top1_title = data[i]["top5_title"][0];
                var top2_title = data[i]["top5_title"][1];
                var top3_title = data[i]["top5_title"][2];
                var top4_title = data[i]["top5_title"][3];
                var top5_title = data[i]["top5_title"][4];
                var ul_ele_but = $("#bottom_row ul:eq(" + i + ")");
                if (i < 4) {
                    var img_ele = $("#top_row .img-col:eq(" + i + ")");
                    var title_ele = $("#top_row h4:eq(" + i + ")");
                    var ul_ele = $("#top_row ul:eq(" + i + ")");
                    var top1_ele = ul_ele.find("li")[0];
                    var top2_ele = ul_ele.find("li")[1];
                    var top3_ele = ul_ele.find("li")[2];
                    var top4_ele = ul_ele.find("li")[3];
                    var top5_ele = ul_ele.find("li")[4];
                    var right_value = data[i]["value"];
                    var top5Arr = data[i]["top5"];
                    var index = top5Arr.indexOf(right_value);
                    if (index < 0) {
                        ul_ele.find("li").attr("class", "wrong");
                        top1_ele.setAttribute("style", "width: " + top1res + "%");
                        top2_ele.setAttribute("style", "width: " + top2res + "%");
                        top3_ele.setAttribute("style", "width: " + top3res + "%");
                        top4_ele.setAttribute("style", "width: " + top4res + "%");
                        top5_ele.setAttribute("style", "width: " + top5res + "%");
                    } else {
                        ul_ele.find("li").attr("class", "wrong");
                        var top_right = ul_ele.find("li")[index];
                        top_right.className = "right";
                        top1_ele.setAttribute("style", "width: " + top1res + "%");
                        top2_ele.setAttribute("style", "width: " + top2res + "%");
                        top3_ele.setAttribute("style", "width: " + top3res + "%");
                        top4_ele.setAttribute("style", "width: " + top4res + "%");
                        top5_ele.setAttribute("style", "width: " + top5res + "%");
                    }
                    img_ele.attr("src", img);
                    title_ele.text(title);
                    var top1 = "&nbsp;&nbsp;" + "<span>" + top1res + "</span>&nbsp;<span>" + top1_title + "</span>";
                    var top2 = "&nbsp;&nbsp;" + "<span>" + top2res + "</span>&nbsp;<span>" + top2_title + "</span>";
                    var top3 = "&nbsp;&nbsp;" + "<span>" + top3res + "</span>&nbsp;<span>" + top3_title + "</span>";
                    var top4 = "&nbsp;&nbsp;" + "<span>" + top4res + "</span>&nbsp;<span>" + top4_title + "</span>";
                    var top5 = "&nbsp;&nbsp;" + "<span>" + top5res + "</span>&nbsp;<span>" + top5_title + "</span>";
                    top1_ele.innerHTML = top1;
                    top2_ele.innerHTML = top2;
                    top3_ele.innerHTML = top3;
                    top4_ele.innerHTML = top4;
                    top5_ele.innerHTML = top5;
                } else {
                    var img_ele = $("#bot_row .img-col:eq(" + (i % 4) + ")");
                    var title_ele = $("#bot_row h4:eq(" + (i % 4) + ")");
                    var ul_ele = $("#bot_row ul:eq(" + (i % 4) + ")");
                    var top1_ele = ul_ele.find("li")[0];
                    var top2_ele = ul_ele.find("li")[1];
                    var top3_ele = ul_ele.find("li")[2];
                    var top4_ele = ul_ele.find("li")[3];
                    var top5_ele = ul_ele.find("li")[4];
                    var right_value = data[i]["value"];
                    var top5Arr = data[i]["top5"];
                    var index = top5Arr.indexOf(right_value);
                    if (index < 0) {
                        ul_ele.find("li").attr("class", "wrong");
                        top1_ele.setAttribute("style", "width: " + top1res + "%");
                        top2_ele.setAttribute("style", "width: " + top2res + "%");
                        top3_ele.setAttribute("style", "width: " + top3res + "%");
                        top4_ele.setAttribute("style", "width: " + top4res + "%");
                        top5_ele.setAttribute("style", "width: " + top5res + "%");
                    } else {
                        ul_ele.find("li").attr("class", "wrong");
                        var top_right = ul_ele.find("li")[index];
                        top_right.className = "right";
                        top1_ele.setAttribute("style", "width: " + top1res + "%");
                        top2_ele.setAttribute("style", "width: " + top2res + "%");
                        top3_ele.setAttribute("style", "width: " + top3res + "%");
                        top4_ele.setAttribute("style", "width: " + top4res + "%");
                        top5_ele.setAttribute("style", "width: " + top5res + "%");
                    }
                    img_ele.attr("src", img);
                    title_ele.text(title);
                    var top1 = "&nbsp;&nbsp;" + "<span>" + top1res + "</span>&nbsp;<span>" + top1_title + "</span>";
                    var top2 = "&nbsp;&nbsp;" + "<span>" + top2res + "</span>&nbsp;<span>" + top2_title + "</span>";
                    var top3 = "&nbsp;&nbsp;" + "<span>" + top3res + "</span>&nbsp;<span>" + top3_title + "</span>";
                    var top4 = "&nbsp;&nbsp;" + "<span>" + top4res + "</span>&nbsp;<span>" + top4_title + "</span>";
                    var top5 = "&nbsp;&nbsp;" + "<span>" + top5res + "</span>&nbsp;<span>" + top5_title + "</span>";
                    top1_ele.innerHTML = top1;
                    top2_ele.innerHTML = top2;
                    top3_ele.innerHTML = top3;
                    top4_ele.innerHTML = top4;
                    top5_ele.innerHTML = top5;
                }
            }
        });
    }

    $("#pf_ul li").bind("click", function () {
        var a = $(this).find("a");
        var span = $("#pf_btn span:eq(0)");
        span.text(a.text());
        if (a.text() == "CPU") {
            $("#power_title").text("CPU Power");
            $("#c_power").show();
            $("#b_power").hide();
        } else if (a.text() == "GPU") {
            $("#c_power").hide();
            $("#b_power").hide();
        } else if (a.text() == "NVIDIA") {
            $("#power_title").text("NVIDIA Power");
            $("#c_power").show();
            $("#b_power").hide();
        } else {
            $("#c_power").show();
            $("#b_power").show();
            $("#power_title").text("Myx Power");
        }
    });

    $("#network_ul li").bind("click", function () {
        var a = $(this).find("a");
        var span = $("#network_btn span:eq(0)");
        span.text(a.text());
    });

    flag = true;
    $("#play_btn").click(function () {
        if (flag) {
            flag = false;
            var pf_span = $("#pf_btn span:eq(0)");
            var network_span = $("#network_btn span:eq(0)");
            $.post("/data/", {
                "playFlag": "1",
                "pf": pf_span.text(),
                "network": network_span.text(),
            }, function () {
                console.log("play success.")
            });
            t = setInterval(getData, 1000);
            console.log(t);
        }
    });

    $("#pause_btn").click(function () {
        $.post("/data/", {
            "stopFlag": "1",
        }, function () {
            console.log("pause success.");
        });
        window.clearInterval(t);
        flag = true;
    });

    $("#stop_btn").click(function () {
        $.post("/data/", {
            "stopFlag": "1",
        }, function () {
            console.log("stop success.");
            location.reload();
        });
    });
});
