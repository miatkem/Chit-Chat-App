import * as React from 'react';

import { Socket } from './Socket';


function handleSubmit(event) {
   var textbar = document.getElementById("tb");
   
   Socket.emit('send message', {
        'message': textbar.value,
        'timestamp': '4/25/20',
        'id': Socket.id
    });
   
   textbar.value = '';
   event.preventDefault();
}

export function MessageInput() {
    React.useEffect(() => {
        Socket.on('current user', (clients) => {
            if (Socket.id in clients && clients[Socket.id]["online"] == true){
                document.getElementById("messageBtn").style.pointerEvents = "auto";
                document.getElementById("tb").placeholder = "Type a message here";
            } else {
                document.getElementById("messageBtn").style.pointerEvents = "none";
                document.getElementById("tb").placeholder = "You must login before sending a message";
            }
        });
    });
    
    return (
        <form onSubmit={handleSubmit} className='messageinput'>
            <input type="text" id="tb" placeholder="You must login before sending a message" />
            <button id="messageBtn">Send</button>
        </form>
    );
}