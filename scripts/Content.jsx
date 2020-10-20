    
import * as React from 'react';
import { Socket } from './Socket';
import { UserList } from './UserList';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { UserName } from './UserName';

export function Content() {
    const [messages, setState] = React.useState(0);
    
    return (
        <div>
            <UserList />
            <div className='chat'>
                <UserName />
                <MessageList />
                <MessageInput />
            </div>
        </div>
    );
}
