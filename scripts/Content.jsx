import * as React from 'react';
import UserList from './UserList';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import UserName from './UserName';

export default function Content() {
  return (
    <div>
      <UserList />
      <div className="chat">
        <UserName />
        <MessageList />
        <MessageInput />
      </div>
    </div>
  );
}
