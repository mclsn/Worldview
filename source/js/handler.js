window.onload = function(){
	if((document.querySelector("#im_contain")) !== null){
		RealTime.Message();
	}
	return false;	
}

document.body.addEventListener("keydown", function(e){
	if(e.target.id == "im_contain_message_textarea"){
		if (e.which == '13') {
			RealTime.SendMessage();
		}		
	}
});

document.body.addEventListener("click", function(e) {
	event = e;

	for (var k in event.path){
		el = event.path[k];
	    if (el.nodeName == "A" && !(el.hasAttribute("onclick"))) {
	    	 e.preventDefault();
	    	 elem = event.path[k];
	    	 window.history.pushState('', '', elem.pathname + elem.search);
	         Core.EngineGet(elem.pathname + elem.search, Data.Loader)
	         break;
	    }
	    else if(el.nodeName == "BUTTON" && !(el.hasAttribute("onclick"))){
	    	if(el.id == "im_contain_message_sender"){
	    		RealTime.SendMessage();
	    	}
	    }
	}

	return false;

});

document.body.addEventListener("change", function(e) {
	elem = e.target;

	if (elem.nodeName == "SELECT") {

		alp = function(target){
			var element = document.getElementById('user_birth_day');
			for(var i = 28; i <= 30; i++){
				if(element[i] == undefined && i < target){
					element.options[element.options.length] = new Option(i+1, i);
				}
				else if(element[i] && i >= target){
					element.remove(i);
					i--;
				}
			}
		}

		e.preventDefault();
		_c0 = ['4','6','9','11'];
		_c1 = ['1','3','5','7','8','10','12'];

		if(elem.id == "user_birth_month"){
			if(_c0.indexOf(elem.value) >= 0) alp(30);
			else if(_c1.indexOf(elem.value) >= 0) alp(31);
			else if(elem.value == 2) alp(29);
		}
	}

	return false;

});