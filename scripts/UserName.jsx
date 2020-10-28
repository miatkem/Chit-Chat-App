import * as React from 'react';
import { Socket } from './Socket';
import GoogleButton from './GoogleButton';

export default function UserName() {
  const [name, setName] = React.useState('Guest');
  const [pic, setPic] = React.useState('https://www.ibts.org/wp-content/uploads/2017/08/iStock-476085198.jpg');

  React.useEffect(() => {
    Socket.on('current userlist', (users) => {
      if (Socket.id in users) {
        setName(users[Socket.id].name);
        setPic(users[Socket.id].pic);
      }
    });
  });

  return (
    <form className="username">
      <img alt="profile" src={pic} className="profPic" />
      <p id="nameInput">{name}</p>
      <GoogleButton />
    </form>
  );
}
