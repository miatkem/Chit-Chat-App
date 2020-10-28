import * as React from 'react';
import GoogleLogin from 'react-google-login';
import { Socket } from './Socket';

function handleSubmit(response) {
  // TODO replace with name from oauth
  const name = response.profileObj.givenName;
  const { email } = response.profileObj;
  const profilePicture = response.profileObj.imageUrl;

  Socket.emit('new google user', {
    id: Socket.id,
    user: name,
    email,
    pic: profilePicture,
  });
}

export default function GoogleButton() {
  return (
    <GoogleLogin
      clientId="829909914851-6dnd3po5vfkgg3nbvm2jc75n31g9vvc0.apps.googleusercontent.com"
      render={(renderProps) => (
        <button type="button" onClick={renderProps.onClick} disabled={renderProps.disabled}>Login!</button>
      )}
      buttonText="Login"
      onSuccess={handleSubmit}
      onFailure={handleSubmit}
      cookiePolicy="single_host_origin"
    />
  );
}

// client ID
// 829909914851-6dnd3po5vfkgg3nbvm2jc75n31g9vvc0.apps.googleusercontent.com
// client secret
// N9TyWZBmrxyBh4YR6TQcZT38
