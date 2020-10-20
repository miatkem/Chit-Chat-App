import * as React from 'react';
import Parser from 'html-react-parser';
import { Socket } from './Socket';

export function UserList() {
    const [users, setUsers] = React.useState({});
    
    React.useEffect(() => {
        Socket.on('current userlist', (clients) => {
            var textbar = document.getElementById("nameInput");
            setUsers(clients);
            return () => {
                 Socket.off('current userlist');
            }
        });
    });
    
    function getUsersInHTML(){
        var ret='';
        for (var key in users) {
            ret+='<li>'+users[key]+'</li>';
        }
        return Parser(ret);
    }
    
    return (
        <div className='userlist'>
            <p><b>Users In Chat:</b></p>
            <ul>
             {getUsersInHTML()}
            </ul>
        </div>
    );
}