var io = require('socket.io').listen(8001);

io.on('connection', function(socket){
  console.log('SOMEONE CONNECTED:', socket.id);

  socket.on('message', function(data){
    console.log(data);
    io.sockets.emit('message', data);
  });

});