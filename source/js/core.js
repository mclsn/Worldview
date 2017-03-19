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

	EngineStaticFile : function(target, callback, preparedData, selector) {
		preparedData = preparedData || null;
		if(target){
			var req = Core.getXmlHttp()         

			req.onreadystatechange = function() {
				if (req.readyState == 4) { 
					if(req.status == 200){
						console.log("[EngineGet]: callback");
						_return = []

						if(selector == "#viewer_wrap"){
							_return.push({'act' : 'viewer'});
						}

						_return.push({'act' : 'add', 'data' : req.responseText, 'selector' : String(selector)});

						if(preparedData){
							_return.push(preparedData);
						}
						callback(JSON.stringify(_return));
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
							//console.log("[EnginePost]: " + req.responseText)
						}
					}
					else{
						console.log("Error EngineGet: status " + req.status);
						console.log(req.responseText)
					}
				}
			}

			req.open('POST', target, true);
			req.setRequestHeader("Content-type", type)
			req.setRequestHeader("X-Requested-With", "XMLHttpRequest");

			req.send(data);
		}
	},

	EnginePut : function(target, callback, data, boundary) {
		if(target && data){
			var req = Core.getXmlHttp()         

			req.open('POST', target, true);
			req.setRequestHeader('Content-type', 'multipart/form-data; boundary="' + boundary + '"');
			req.setRequestHeader("X-Requested-With", "XMLHttpRequest");
			req.setRequestHeader('Cache-Control', 'no-cache');

			if (!XMLHttpRequest.prototype.sendAsBinary) {
	            XMLHttpRequest.prototype.sendAsBinary = function(datastr) {
	                function byteValue(x) {
	                    return x.charCodeAt(0) & 0xff;
	                }
	                var ords = Array.prototype.map.call(datastr, byteValue);
	                var ui8a = new Uint8Array(ords);
	                this.send(ui8a.buffer);
	            }
	        }

			req.upload.onprogress = function(event) {
				document.querySelector("div#main_progressBar").style.width = String(100 * event.loaded / event.total) + "vw";
			}

			req.onreadystatechange = function() {  
				if (req.readyState == 4) {

					setTimeout(
						function(){document.querySelector("div#main_progressBar").style.width = "0vw"}
						, 1000)

					if(req.status == 200){
						if(callback){
							console.log("[EnginePut]: callback");
							callback(req.responseText);
						}
						else{
							console.log("[EnginePut]: success");
							//console.log("[EnginePut]: " + req.responseText)
						}
					}
					else{
						console.log("Error EnginePut: status " + req.status);
						//console.log(req.responseText)
					}
				}
			}

			if(req.sendAsBinary) {
            	req.sendAsBinary(data);
        	}
        	else{
            	req.send(data);
        	}
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

	UploadPhoto : function(event, obj){
		_valid = ['user_avatar', 'csrf']
		event.preventDefault();

		var input = document.querySelector('input[type="file"]#user_avatar');
		var csrf = document.querySelector('input#csrf').value;

		file = input.files[0];
		var putSender = new FileReader();
		//var getImage = new FileReader();

		//getImage.onload = function(event) {
		//	preparedData = {'act' : 'attr', 'data' : event.target.result, 'selector' : '#edit_photoUpload_img', 'type' : 'src'};
		//	Core.EngineStaticFile('/sys/editPhotoUpload.html', Data.Loader, preparedData, '#viewer_wrap');
		//	putSender.readAsBinaryString(file);
		//};

		putSender.onload = function(){
			var boundary = "0xf53g5";
			var body = "--" + boundary + "\r\n";
				body += "Content-Disposition: form-data; name=\"user_avatar\"; filename=\"" + unescape(encodeURIComponent(file.name)) + "\"\r\n";
	        	body += "Content-Type: application/octet-stream\r\n\r\n";
	        	body += putSender.result + "\r\n";
	        	body += "--" + boundary + "\r\n";
		        body += "Content-Disposition: form-data; name=\"csrf\"\r\n\r\n"; // unescape позволит отправлять файлы с русскоязычными именами без проблем.
		        body += csrf + "\r\n";
		        body += "--" + boundary + "--";

			Core.EnginePut('/edit', Data.Loader, body, boundary);
			input.value = null;
		};
		putSender.readAsBinaryString(file);
		//getImage.readAsDataURL(file);

		return false; 
	},

	Edit : function(event, obj){
		_valid = ['first_name', 'last_name', 'csrf', 'user_name', 'user_birth_day', 'user_birth_month', 'user_birth_year']
		_error = ['', '', ''];
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
			Core.EnginePost('/edit', Data.Loader, multipart[0], 'multipart/form-data; boundary=' + multipart[1])
			
		}
		catch(e){
			console.log(e)
		}

		return false; 
	},

	Logout : function(event, obj){
		event.preventDefault();
		var urlParams = new URLSearchParams(obj.search);
		try{
			var csrf = urlParams.get('csrf');
			multipart = Core.MultipartData({'csrf' : encodeURIComponent(csrf)});
			Core.EnginePost('/logout', Data.Loader, multipart[0], 'multipart/form-data; boundary=' + multipart[1])
		}
		catch(e){
			console.log(e)
		}

		return false; 
	}
}

var Data = {

	Viewer : function(data){
		var element = document.getElementById('viewer_wrap');
		if(element){
			parentElem.removeChild(elem)
		}
		else{
			data = data || null;
			var div = document.createElement('div');
			div.id = "viewer_wrap";
			if(data)
				div.innerHTML = data;
			document.body.appendChild(div);			
		}
		console.log("[Viewer]: end")
		return false;
	},

	Loader : function(data){
		console.log(data)
		try{
			data = JSON.parse(data);
			console.log(data)
			data.forEach(function(entry) {
				console.log(entry.act);
				if(entry.act == "viewer"){
					Data.Viewer();				
				}
				else if(entry.act == "add"){
					targetBlock = document.querySelector(entry.selector)
					console.log(entry.selector)
					console.log(targetBlock)
					targetBlock.innerHTML = entry.data;
				}
				else if(entry.act == "attr"){
					targetBlock = document.querySelector(entry.selector)
					console.log(entry.selector)
					targetBlock[entry.type] = entry.data;
				}
				else if(entry.act == "reload"){
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