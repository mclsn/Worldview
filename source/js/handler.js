document.body.addEventListener("click", function(e) {
	event = e;

	for (var k in event.path){
		el = event.path[k];
	    if (el.nodeName == "A" && !(el.hasAttribute("onclick"))) {
	    	 e.preventDefault();
	    	 elem = event.path[k];
	    	 window.history.pushState('', '', elem.pathname + elem.search);
	         Core.EngineGet(elem.pathname + elem.search, Data.loader)
	         break;
	    }
	}

	return false;

});