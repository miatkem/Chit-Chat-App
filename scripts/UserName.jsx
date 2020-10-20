import * as React from 'react';
import { Socket } from './Socket';
import { GoogleButton } from './GoogleButton';


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
        Socket.on('current userlist', (users) => {
            setName(users[Socket.id].name);
        });
    });
        
    return (
        <form className='username'>
            <label htmlFor="nameInput">Your Name:</label>
            <p id='nameInput'>{name}</p>
            <GoogleButton />
        </form>
    );
}