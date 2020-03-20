var everyPageDataCount = 7;
var postPageIndex = 0;
var postAllPage = 0;
$(document).ready(function () {

    var searchNameVal = $("#SEARCH_POST_NAME_HIDDEN").val().trim();
    getPostList(searchNameVal, 0, everyPageDataCount, true, "/postbar/userManageController/getUserList");

    var regage = $("#regAge");
    var selectPotion = $("#regAge option");

    if (selectPotion.length == "0") {
        for (var i = 14; i < 100; i++) {
            regage.append("<option value='" + i + "'>" + i + "</option>");
        }
    }

});

function getPostList(postTitle, pageIndex, everyPageDataCount, SynOrAsyn, url) {

}


function showPostlist(registerList, postAllNum, allPage, pageIndex) {

}
function JumpPage(page) {
    var searchNameVal = $("#SEARCH_POST_NAME").val().trim();
    if(searchNameVal){
        window.location.href="/userManage/?userName="+searchNameVal+"&&page="+page
    }else{
        window.location.href="/userManage/?page="+page
    }
}

function GOTO_POST_NEXT_PAGE() {

    var searchNameVal = $("#SEARCH_POST_NAME_HIDDEN").val().trim();
    getPostList(searchNameVal, postPageIndex + 1, everyPageDataCount, true, "/postbar/userManageController/getUserList");
}

function GOTO_POST_TAIL_PAGE() {
    var searchNameVal = $("#SEARCH_POST_NAME_HIDDEN").val().trim();
    getPostList(searchNameVal, postAllPage - 1, everyPageDataCount, true, "/postbar/userManageController/getUserList");
}

function GOTO_POST_PAGE(maxpage) {
    var jumpVal = $("#JUMP_INPUT_ID").val().trim();
    if (jumpVal === "") {
        $.MsgBox.Alert("消息", "跳转页不能为空");
        return;
    }
    if (!(/^[0-9]+$/.test(jumpVal))) {
        $.MsgBox.Alert("消息", "页码必须为数字");
        return;
    }
    if (jumpVal <= 0) {
        $.MsgBox.Alert("消息", "页码必须大于等于1");
        return;
    }
    if (jumpVal > maxpage) {
        $.MsgBox.Alert("消息", "页码超出上限");
        return;
    }
    JumpPage(jumpVal)
}


function GOTO_POST_HOME_PAGE() {
    var searchNameVal = $("#SEARCH_POST_NAME_HIDDEN").val().trim();
    getPostList(searchNameVal, 0, everyPageDataCount, true, "/postbar/userManageController/getUserList");
}

function GOTO_POST_PREVIOUS_PAGE() {
    var searchNameVal = $("#SEARCH_POST_NAME_HIDDEN").val().trim();
    getPostList(searchNameVal, postPageIndex - 1, everyPageDataCount, true, "/postbar/userManageController/getUserList");

}

function searchByPostName() {
    var searchNameVal = $("#SEARCH_POST_NAME").val().trim();
	window.location.href="/userManage/?userName="+searchNameVal
    // getPostList(searchNameVal, 0, everyPageDataCount, true, "/postbar/userManageController/getUserList");
}

function DELETE_POST() {
    var chk_value = [];
    $('input[name="DELETE_CHECK_NAME"]:checked').each(function () {
        chk_value.push($(this).val());
    });
    if (chk_value.length == 0) {
        $.MsgBox.Alert("消息", "请先选择需要删除的用户");
        return;
    }
    $.ajax({
        url: "/userManage/",
        type: "DELETE",
        data: {
            "csrfmiddlewaretoken": '{{ csrf_token }}',
            "chk_values": chk_value,
        },
        dataType: "JSON",
        success: function (result) {
            if (result['status']) {
                $.MsgBox.Alert("消息", "删除成功");
                window.location.reload()
            } else {
                $.MsgBox.Alert("消息", result["message"]);
            }
        }
    })


}

function editUserCheck() {
    var userUUID = $("#userUUID").val();
    var userName = $("#userName").val();
    var regsex = $("#regsex").val();
    var regAge = $("#regAge").val();
    var regEmial = $("#regEmial").val();
    var admin = $("#admin").val();
    var password = $("#password").val();
    var oldName = $("#oldUserName").val();
    if (typeof (userName) == 'undefined' || userName.trim() == "") {
        $("#tishi").html("用户名不能为空");
        return;
    }
    if (userName.trim().length > 20) {
        $("#tishi").html("用户名不能大于20个字符");
        return;
    }

    if (password.trim() != "" && password.trim().length != 6) {
        $("#tishi").html("密码必须为6位");
        return;
    }


    if (typeof (regEmial) == 'undefined' || regEmial.trim() == "") {
        $("#tishi").html("邮箱地址不能为空");
        return;
    }

    if (!(/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(regEmial.trim()))) {
        $("#tishi").html("邮箱地址格式不正确");
        return false;
    }

    $.ajax({
        url: "/userManage/",
        type: "PUT",
        data: {
            "csrfmiddlewaretoken": '{{ csrf_token }}',
            "id": userUUID,
            "userName": userName,
            "regsex": regsex,
            "regAge": regAge,
            "regEmail": regEmial,
            "role": admin,
            "oldName": oldName,
            "password": password
        },
        dataType: "JSON",
        success: function (result) {
            if (result['status']) {
                $.MsgBox.Alert("消息", "修改成功");
                window.location.reload()
            } else {
                $.MsgBox.Alert("消息", result["message"]);
            }
        }
    })

    // $("#userUUID").val("");
    // $("#userName").val("");
    // $("#regsex").val("");
    // $("#regAge").val("");
    // $("#regEmial").val("");
    // $("#admin").val("");
    // $("#password").val("");
    // $("#oldUserName").val("");
    // $("#tishi").html("");
    // $("#POST_LIST_DIV_ID").attr("style", "display:block;");//隐藏div
    // $("#POST_ADD_DIV_ID").attr("style", "display:none;");//隐藏div
    // var searchNameVal = $("#SEARCH_POST_NAME_HIDDEN").val().trim();
    // getPostList(searchNameVal, 0, everyPageDataCount, true, "/postbar/userManageController/getUserList");


}

function returnPostList() {
    $("#userUUID").val("");
    $("#userName").val("");
    $("#regsex").val("");
    $("#regAge").val("");
    $("#regEmial").val("");
    $("#admin").val("");
    $("#password").val("");
    $("#oldUserName").val("");
    $("#tishi").html("");
    $("#POST_LIST_DIV_ID").attr("style", "display:block;");//隐藏div
    $("#POST_ADD_DIV_ID").attr("style", "display:none;");//隐藏div
}

function EDIT_USER(userUUID, userName, regsex, regAge, regEmial, admin) {

    $("#POST_LIST_DIV_ID").attr("style", "display:none;");//隐藏div
    $("#POST_ADD_DIV_ID").attr("style", "display:block;");//隐藏div

    $("#userUUID").val(userUUID);
    $("#userName").val(userName);
    $("#regsex").val(regsex);
    $("#regAge").val(regAge);
    $("#regEmial").val(regEmial);
    $("#admin").val(admin);
    $("#oldUserName").val(userName);
}