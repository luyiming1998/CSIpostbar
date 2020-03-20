// $(document).ready(function () {
//
//
//
// 	         	var regage=$("#regAge");
//
// 	         	for(var i=14;i<100;i++){
// 	             	regage.append("<option value='"+i+"'>"+i+"</option>");
// 	             }
// 	         	 $("#regUUID").val("{{user.id}}");
// 	             $("#userName").val("{{user.userName}}");
// 	    		 $("#regSex option[value='" + 0 + "']").attr("selected", true);
// 	    		 $("#regAge option[value='" + 40 + "']").attr("selected", true);
// 	    		 $("#regEmial").val("11@163.com");
// 	    		 $("#oldUserName").val("sjm");
//
//
// });


function subReg(){
	var regUUID=$("#regUUID").val();
	var userName=$("#userName").val();
	var regSex=$("#regSex").val();
	var regAge=$("#regAge").val();
	var regEmial=$("#regEmial").val();
	var oldName=$("#oldUserName").val();
	if(typeof (userName) == 'undefined' || userName.trim()=="" ){
		$("#tishi").html("用户名不能为空");
		return;
	}
	if(userName.trim().length>20){
		$("#tishi").html("用户名不能大于20个字符");
		return;
	}
	

	if(typeof (regEmial) == 'undefined' || regEmial.trim()==""){
		$("#tishi").html("邮箱地址不能为空");
		return;
	}

	if(!(/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(regEmial.trim()))){
		$("#tishi").html("邮箱地址格式不正确");
		return false;
	}
	    $.ajax({
        url: "/perSet/",
        type: "PUT",
        data: {
            "csrfmiddlewaretoken": '{{ csrf_token }}',
            "id": regUUID,
            "userName": userName,
            "regsex": regSex,
            "regAge": regAge,
            "regEmail": regEmial,
            "oldName": oldName,
        },
        dataType: "JSON",
        success: function (result) {
            if (result['status']) {
                $.MsgBox.Alert("消息", "修改成功");
				 window.parent.location.replace("/logout/");
            } else {
                $.MsgBox.Alert("消息", result["message"]);
            }
        }
    })

	


}