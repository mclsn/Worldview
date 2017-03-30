// Создаем текст сообщений для событий
strings = {
	'connected': '[sys][time]%time%[/time]: Вы успешно соединились к сервером как [user]%name%[/user].[/sys]',
	'userJoined': '[sys][time]%time%[/time]: Пользователь [user]%name%[/user] присоединился к чату.[/sys]',
	'messageSent': '[out][time]%time%[/time]: [user]%name%[/user]: %text%[/out]',
	'messageReceived': '[in][time]%time%[/time]: [user]%name%[/user]: %text%[/in]',
	'userSplit': '[sys][time]%time%[/time]: Пользователь [user]%name%[/user] покинул чат.[/sys]'
};

window.onload = function() {
	socket = io.connect('http://192.168.1.9:8080');
	socket.on('connect', function () {
		socket.on('message', function (msg) {
			console.log(msg);
			document.querySelector('#im_log').innerHTML += msg;
			document.querySelector('#im_log').scrollTop = document.querySelector('#im_log').scrollHeight;
		});
		document.querySelector('#im_contain_message_textarea').onkeypress = function(e) {
			if (e.which == '13') {
				socket.send(escape(document.querySelector('#im_contain_message_textarea').value));
				document.querySelector('#im_contain_message_textarea').value = '';
			}
		};
		document.querySelector('#im_contain_message_sender').onclick = function() {
			socket.send(escape(document.querySelector('#im_contain_message_textarea').value));
			document.querySelector('#im_contain_message_textarea').value = '';
		};		
	});
};