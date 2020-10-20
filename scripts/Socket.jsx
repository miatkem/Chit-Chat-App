import * as SocketIO from 'socket.io-client';

export var Socket = SocketIO.connect();

Socket.on('connect', () => {
  Socket.emit('i am here', Socket.id);
});

Socket.on('who is here', () => 
    Socket.emit('i am here',Socket.id));