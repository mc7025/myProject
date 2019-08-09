$(document).ready(function () {
    $("#yes_btn").click(function () {
        var h_ip = $("#host_ip").val();
        var h_os = $("#host_os option:selected").text();
        var h_username = $("#host_username").val();
        var h_password = $("#host_password").val();
        var h_id = $("#host_id").val();
        $.ajax('/HostModels/', {
            dataType: "json",
            type: "PUT",
            data: {
                "h_id": h_id,
                "h_ip": h_ip,
                "h_os": h_os,
                "h_username": h_username,
                "h_password": h_password,
            },
            success: function () {
                window.location.href = "/hosts/";
            },
        });
    });

    $("#btn").click(function () {
        btnFun();
    });

    blurFun();

    baseLiFun("hosts_li");
});