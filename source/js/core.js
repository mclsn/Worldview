__socket = null;

var Sys = {

	_logTimer : (new Date()).getTime(),

	console : function(msg){
		var t = '[' + (((new Date()).getTime() - this._logTimer) / 1000) + '] ';
		console.log(t + ": " + String(msg));	
	},

	jsonToParam : function(obj){
		var str = Object.keys(obj).map(function(key){ 
			return encodeURIComponent(key) + '=' + encodeURIComponent(obj[key]); 
		}).join('&');
		return str;
	},

	csrf : function(){
		Core.EnginePost('/api', Data.Loader, null)
	},

	HtmlEncode : function(s){
		var el = document.createElement("div");
		el.innerText = el.textContent = s;
		s = el.innerHTML;
		return s;
	}

}

var RealTime = {

	Message : function(){

		strings = {
			'connected': '[sys][time]%time%[/time]: Вы успешно соединились к сервером как [user]%name%[/user].[/sys]',
			'userJoined': '[sys][time]%time%[/time]: Пользователь [user]%name%[/user] присоединился к чату.[/sys]',
			'messageSent': '[out][time]%time%[/time]: [user]%name%[/user]: %text%[/out]',
			'messageReceived': '[in][time]%time%[/time]: [user]%name%[/user]: %text%[/in]',
			'userSplit': '[sys][time]%time%[/time]: Пользователь [user]%name%[/user] покинул чат.[/sys]'
		};

		if(__socket)
			__socket.disconnect('http://192.168.1.200:8001')
		__socket = io.connect('http://192.168.1.200:8001');

		__socket.on('connect', function () {
			__socket.on('message', function (data) {
				try{
					data = JSON.parse(data);
					console.log(data.user_fullname);
					document.querySelector('#im_log').innerHTML += 
						"<div class='im_contain_messageUser'>" + 
							"<img src='/usr/av/" + data.user_avatar + ".jpg'>" +
							"<div>" +
								"<span>" + data.user_fullname + "</span>"+
								"<div>" + data.msg + "</div>"+
							"</div>" +
						"</div>";
				}
				catch(e){
					console.log(e);
				}
			});
		});

		return false;

	},

	SendMessage : function(){
		elem = document.querySelector('#im_contain_message_textarea');
		multipart = Core.MultipartData({'data' : Sys.HtmlEncode(elem.value)});
		Core.EnginePost('/msg', console.log, multipart[0], 'multipart/form-data; boundary=' + multipart[1])
		elem.value = '';
		document.querySelector('#im_log').scrollTop = document.querySelector('#im_log').scrollHeight;
		elem.focus();
		return false;
	}

}

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
					Sys.console("EngineStaticFile -end with status " + req.status)
					
					if(req.status == 200){
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
					Sys.console("EngineGet -end with status " + req.status)

					if(req.status == 200 && callback){
						callback(req.responseText, true);
					}
					else{
						console.log(req.responseText);
					}
				}
			}

			req.open('GET', target, true);  
			req.setRequestHeader("X-Requested-With", "XMLHttpRequest");
			req.send(null);
			return false;
		}
	},

	EnginePost : function(target, callback, sendData, typer) {
		if(target){
			type = typer || 'application/x-www-form-urlencoded';
			data = sendData || null;

			var req = Core.getXmlHttp()         

			req.onreadystatechange = function() {  
				if (req.readyState == 4) { 
					Sys.console("EnginePost -end with status " + req.status)
					if(req.status == 200) {
						if(data && callback) callback(req.responseText, true);
						else if(callback) callback(req.responseText, false);
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
					Sys.console("EnginePut -end with status " + req.status)
					
					if(req.status == 200){
						if(callback){
							callback(req.responseText, true);
						}
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

	AddFriend : function(obj, uid, csrf){
		data = {"csrf" : csrf, "uid" : uid, "act" : "addfriend"};
		Core.EngineGet('/api?' + Sys.jsonToParam(data), Data.Loader);
	},

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

	Logout : function(event, csrf){
		try{
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
		return false;
	},

	Loader : function(data, csrf){
		Sys.console("Loader -start")
		try{
			console.log(data)
			data = JSON.parse(data);
			data.forEach(function(entry) {
				if(entry.act == "viewer"){
					Data.Viewer();				
				}
				else if(entry.act == "add"){
					targetBlock = document.querySelector(entry.selector);
					targetBlock.innerHTML = entry.data;
				}
				else if(entry.act == "attr"){
					if('selector' in entry){
						targetBlock = document.querySelector(entry.selector)
						targetBlock[entry.type] = entry.data;
					}
					else if('selectors' in entry){
						targetBlocks = document.querySelectorAll(entry.selectors);
						console.log(targetBlocks);
						targetBlocks.forEach(function(e) {
							if(e.nodeName == ("A" || "BUTTON")){
								e.setAttribute("hash", entry.data);
							}
							else if(e.nodeName == "INPUT"){
								e.setAttribute("value", entry.data);
							}
						});
					}
				}
				else if(entry.act == "callback"){
					console.log(data);
					eval(entry.data);
				}
				else if(entry.act == "reload"){
					window.location.href = "/";
				}
			});

			Sys.console("Loader -end")	
		}
		catch(e){
			//console.log(e)
		}
		//console.log(csrf)
		if(csrf == true) Sys.csrf();
		return false;
	}

}