import * as React from 'react';
import { Socket } from './Socket';


function handleSubmit(event) {
    
   var textbar = document.getElementById("nameInput");
   
   Socket.emit('change name', {
        'user': textbar.value,
        'id': Socket.id
    });
   event.preventDefault();
}

export function UserName() {
    const [name, setName] = React.useState("Guest");
    
    React.useEffect(() => {
        Socket.emit('get userlist');
        Socket.on('current userlist', (users) => {
            var textbar = document.getElementById("nameInput");
            setName(users[Socket.id]);
            textbar.value = name;
            return () => {
            Socket.off('current userlist');
        }
            
        });
        
    });
        
    return (
        <form onSubmit={handleSubmit} className='username'>
            <label for="nameInput">Your Name:</label>
            <input type="text" id="nameInput" />
            <button>Change Name</button>
        </form>
    );
}