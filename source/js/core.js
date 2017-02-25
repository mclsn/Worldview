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


	Ajax : function() {

		var req = getXmlHttp()         
		
		req.onreadystatechange = function() {  
			if (req.readyState == 4) { 
				if(req.status == 200) { 
					console.log(req.responseText);
				}
			}
		}

		req.open('GET', '/login', true);  
		req.send(null);
	}
}

var Auth = {

	login : function(event){
		console.log(event);
		return false; 
	}
}
