document.body.addEventListener("click", function(e) {
	event = e;

	for (var k in event.path){
	    if (event.path[k].nodeName == "A") {
	    	 e.preventDefault();
	    	 elem = event.path[k];
	    	 window.history.pushState('', '', elem.pathname + elem.search);
	         Core.EngineGet(elem.pathname + elem.search, Data.loader)
	         break;
	    }
	}

	return false;

});