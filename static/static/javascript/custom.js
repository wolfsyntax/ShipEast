/*function sys_timer(){
//	var x = document.getElementById("timeDiff").innerText;
//	document.getElementById("timeDiff").innerHTML = x;
  	//alert("test" + x);
  var today = new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  h = checkTime(h);
  m = checkTime(m);
  s = checkTime(s);
  document.getElementById('timeDiff').innerHTML =
  h + ":" + m + ":" + s;
//  var t = setTimeout(startTime, 500);

   	var t = setTimeout(sys_timer, 500);
}

function checkTime(i) {
  if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
  return i;
}

/*	function toggler() {
        $('#sidebar').toggleClass('active');
        $('#body-container').toggleClass('active');
       // alert("test");
    }
*/
/*
    $('#sidebarCollapse').on('click', function () {

        $('#sidebar').toggleClass('active');
        $('#body-container').toggleClass('active');
        var x = $("#toggler-icon").attr("class");
        if(x == 'fa fa-arrow-left fa-lg'){
        	$("#toggler-icon").removeClass("fa fa-arrow-left fa-lg").addClass("fa fa-arrow-right fa-lg");
		}else{
        	$("#toggler-icon").removeClass("fa fa-arrow-right fa-lg").addClass("fa fa-arrow-left fa-lg");
		}
		//alert(x);
        //alert("Toggle");
    });

*/
$(document).ready(function(){

	function sys_timer(){
//	var x = document.getElementById("timeDiff").innerText;
//	document.getElementById("timeDiff").innerHTML = x;
  	//alert("test" + x);
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    h = checkTime(h);
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('timeDiff').innerHTML =
    h + ":" + m + ":" + s;
  //  var t = setTimeout(startTime, 500);

     	var t = setTimeout(sys_timer, 500);

  }

  function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
  }

/*	function toggler() {
        $('#sidebar').toggleClass('active');
        $('#body-container').toggleClass('active');
       // alert("test");
    }
*/

  $("#is_agree").change(function(){//alert("Changin");
    if(this.checked){
      $("#reg_submit").removeAttr("disabled");
    }else{
      $("#reg_submit").attr("disabled","disabled");
    }
  });

  $('#sidebarCollapse').on('click', function () {

    $('#sidebar').toggleClass('active');
    $('#body-container').toggleClass('active');
    
    var x = $("#toggler-icon").attr("class");
    
    if(x == 'fa fa-arrow-left fa-lg'){
      $("#toggler-icon").removeClass("fa fa-arrow-left fa-lg").addClass("fa fa-arrow-right fa-lg");
    }else{
      $("#toggler-icon").removeClass("fa fa-arrow-right fa-lg").addClass("fa fa-arrow-left fa-lg");
    }
		//alert(x);
        //alert("Toggle");
  });



});

