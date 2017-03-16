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
						console.log("[EngineGet]: callback");
						callback(req.responseText);
					}
					else{
						console.log("[EngineGet]: success with status " + req.status);
					}
				}
			}

			req.open('GET', target, true);  
			req.setRequestHeader("X-Requested-With", "XMLHttpRequest");
			req.send(null);
			return false;
		}
	},

	EnginePost : function(target, callback, data, typer) {
		if(target && data){
			type = typer || 'application/x-www-form-urlencoded';
			var req = Core.getXmlHttp()         

			req.onreadystatechange = function() {  
				if (req.readyState == 4) { 
					if(req.status == 200){
						if(callback){
							console.log("[EnginePost]: callback");
							callback(req.responseText);
						}
						else{
							console.log("[EnginePost]: success");
							console.log("[EnginePost]: " + req.responseText)
						}
					}
					else{
						console.log("Error EngineGet: status " + req.status);
						console.log(req.responseText)
					}
				}
			}

			req.open('POST', target, true);
			req.setRequestHeader("Content-Type", type)
			req.setRequestHeader("X-Requested-With", "XMLHttpRequest");

			req.send(data);
		}
	},

	MultipartData : function(data){
		var body = [''];
		var boundary = String(Math.random()).slice(2);
		var boundaryMiddle = '--' + boundary + '\r\n';
		var boundaryLast = '--' + boundary + '--\r\n';
		for (var key in data) {
			body.push('Content-Disposition: form-data; name="' + key + '"\r\n\r\n' + data[key] + '\r\n');
		}
		body = body.join(boundaryMiddle) + boundaryLast;
		return [body, boundary];
	}

}

var Profile = {

	Edit : function(event, obj){
		_valid = ['first_name', 'last_name', 'csrf']
		var data = {}

		event.preventDefault();
		try{
			r = document.querySelectorAll('.FormDefault');
			r.forEach(function(entry) {
				if (_valid.indexOf(entry.id) >= 0){
					data[entry.id] = encodeURIComponent(entry.value);
				}
				else{
					throw "[Edit]: error key";
				}
			});
			multipart = Core.MultipartData(data);
			Core.EnginePost('/edit', Data.loader, multipart[0], 'multipart/form-data; boundary=' + multipart[1])
			
		}
		catch(e){
			console.log(e)
		}

		return false; 
	}
}

var Data = {

	loader : function(data){
		try{
			data = (data.replace(/"/g, "\\'")).replace(/'/g, "\"");
			data = JSON.parse(data);
			data.forEach(function(entry) {
				if(entry.act == "add"){
					targetBlock = document.querySelector(entry.selector)
					targetBlock.innerHTML = entry.data;
				}
				if(entry.act == "attr"){
					targetBlock = document.querySelector(entry.selector)
					targetBlock[entry.type] = entry.data;
				}
				if(entry.act == "reload"){
					window.location.href = "/";
				}
			});
		}
		catch(e){
			console.log(e)
		}

		return false;
	}

}