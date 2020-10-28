import * as React from 'react';
import { Socket } from './Socket';
import ReactDOM from 'react-dom';
import GoogleLogin from 'react-google-login';

function handleSubmit(response) {
    // TODO replace with name from oauth
    let name = response.profileObj.givenName;
    let email = response.profileObj.email;
    let profilePicture = response.profileObj.imageUrl;
    
    console.log(name);
    Socket.emit('new google user', {
        'id': Socket.id,
        'user': name,
        'email':email,
        'pic': profilePicture,
    });
}

export function GoogleButton() {
    return <GoogleLogin
        clientId="829909914851-6dnd3po5vfkgg3nbvm2jc75n31g9vvc0.apps.googleusercontent.com"
        render={renderProps => (
          <button onClick={renderProps.onClick} disabled={renderProps.disabled}>Login!</button>
        )}
        buttonText="Login"
        onSuccess={handleSubmit}
        onFailure={handleSubmit}
        cookiePolicy={'single_host_origin'} />;
}

