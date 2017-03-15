var Core = {

	getXmlHttp : function(){
		var xmlhttp;
		try{
			xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
		}
		catch (e){
			try{
				xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
			}
			catch(E){
				xmlhttp = false;
			}
		}
		if (!xmlhttp && typeof XMLHttpRequest!='undefined'){
			xmlhttp = new XMLHttpRequest();
		}
		return xmlhttp;
	},


	EngineGet : function(target, callback) {
		if(target){
			var req = Core.getXmlHttp()         

			req.onreadystatechange = function() {  
				if (req.readyState == 4) { 
					if(req.status == 200){
						console.log("Start Callback: EngineGet");
						callback(req.responseText);
					}
					else{
						console.log("Error EngineGet: status " + req.status);
					}
				}
			}

			req.open('GET', target, true);  
			req.setRequestHeader("X-Requested-With", "XMLHttpRequest");
			req.send(null);
		}
	},

	EnginePost : function(target, callback, data) {
		if(target && data){
			var req = Core.getXmlHttp()         

			req.onreadystatechange = function() {  
				if (req.readyState == 4) { 
					if(req.status == 200){
						if(callback){
							console.log("Start Callback: EngineGet");
							callback(req.responseText);
						}
						else{
							console.log("EnginePost : Success");
						}
					}
					else{
						console.log("Error EngineGet: status " + req.status);
					}
				}
			}

			req.open('POST', target, true);
			req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
			req.setRequestHeader("X-Requested-With", "XMLHttpRequest");
			req.send(data);
		}
	}

}

var Profile = {

	Edit : function(event, obj){
		_valid = ['first_name', 'last_name']
		_data = ""

		event.preventDefault();
		r = document.querySelectorAll('.FormDefault');
		r.forEach(function(entry) {
			if (entry.id in _valid){
				console.log(entry.id);
			}
			else{
				_data += entry.id + "=" + encodeURIComponent(entry.value) + "&"
			}
			console.log(_data);
		});
		Core.EnginePost('/edit', null, _data)
		return false; 
	}
}

var Data = {

	loader : function(data){
		//document.body.innerHTML = data;
		// if(data){
		console.log(data)
		data = data.replace(/"/g, "\\'").replace(/'/g, "\"");
		console.log(data)
		data = JSON.parse(data);
		console.log(data)

		if(data.type == "id"){
			targetBlock = document.getElementById(data.block);
			targetBlock.innerHTML = data.data;
		}


		// 	if(data.sys.type == "id"){
		// 		var xmlhttp = Core.getXmlHttp();
		//          xmlhttp.open("GET", data.sys.page + ".html", true);
		//          console.log(data)
		//          xmlhttp.onreadystatechange = function() {  
		// 			if (xmlhttp.readyState == 4) { 
		// 				if(xmlhttp.status == 200){
		// 					targetBlock = document.getElementById(data.sys.block);
		// 					targetBlock.innerHTML = xmlhttp.responseText;
		// 					data.add.forEach(function(entry) {
		// 						switch(entry.type){
		// 							case 'attr':
		// 								console.log(entry);
		// 								break;
		// 						}
		// 					});
		// 				}
		// 			}
		// 		}
		// 		xmlhttp.send();
		// 	}
		// }
		return false;
	}

}