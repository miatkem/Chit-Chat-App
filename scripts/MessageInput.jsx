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
    return (
        <form onSubmit={handleSubmit} className='messageinput'>
            <input type="text" id="tb" />
            <button>Send</button>
        </form>
    );
}