$(function(){


	 $("#auSetUUID").val("0000000000000");
	 $("#auSetVoiPer option[value='" + 0 + "']").attr("selected", true);
	 $("#auSetSpd option[value='" + 5 + "']").attr("selected", true);
	 $("#auSetPit option[value='" + 5 + "']").attr("selected", true);
	 $("#auSetVol option[value='" + 5 + "']").attr("selected", true);


});

function updateAudioSetUp(){
	var auSetUUID=$("#auSetUUID").val();
	var auSetVoiPer=$("#auSetVoiPer").val();
	var auSetSpd=$("#auSetSpd").val();
	var auSetPit=$("#auSetPit").val();
	var auSetVol=$("#auSetVol").val();


}