import * as React from 'react';
import Parser from 'html-react-parser';
import { Socket } from './Socket';

export default function UserList() {
  const [users, setUsers] = React.useState({});

  React.useEffect(() => {
    Socket.on('current userlist', (clients) => {
      setUsers(clients);
      return () => {
        Socket.off('current userlist');
      };
    });
  });

  function getUsersInHTML() {
    let ret = '';
    for (const key in users) {
      if (users[key].online === true) {
        ret += `<li>${users[key].name}</li>`;
      }
    }
    return Parser(ret);
  }

  return (
    <div className="userlist">
      <p><b>Users In Chat:</b></p>
      <ul>
        {getUsersInHTML()}
      </ul>
    </div>
  );
}
