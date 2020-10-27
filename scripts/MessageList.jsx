import * as React from 'react';
import Parser from 'html-react-parser';
import { Socket } from './Socket';

export default function MessageList() {
  const [messages, setMessages] = React.useState(() => {
    Socket.emit('get messages');
    return [];
  });

  function updateMessages(data) {
    const { msg } = data;
    setMessages(msg);
    const newestMessage = document.getElementById(`msg_${msg.length - 1}`);
    if (msg.length > 0) {
      newestMessage.scrollIntoView();
    }
  }

  React.useEffect(() => {
    Socket.on('messages updated', updateMessages);
    return () => {
      Socket.off('messages updated', updateMessages);
    };
  });

  return (
    <div className="messagelist">
      <ul>
        {
                (messages || []).map(
                  (message, index) => (
                    <li key={`msg_${index}`}>
                      <div className="message" id={`msg_${index}`}>
                        <p className="user"><b>{message.user}</b></p>
                        <div className="messagebox">
                          <p className="messagetext">{Parser(message.message)}</p>
                          <p className="timestamp"><i>{message.timestamp}</i></p>
                        </div>
                      </div>
                    </li>
                  ),
                )
            }
      </ul>
    </div>
  );
}
