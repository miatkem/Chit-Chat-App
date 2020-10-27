import os, sys
import flask
import flask_socketio
import flask_sqlalchemy
import msgParser
from bot import bot

from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone



TIME_ZONE = timezone('US/Eastern');

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

sql_user = os.environ['SQL_USER']
sql_pwd = os.environ['SQL_PASSWORD']
dbuser = os.environ['USER']
database_uri = os.environ['DATABASE_URL']


app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = flask_sqlalchemy.SQLAlchemy()
import models


def init_db(app):
    db.init_app(app)
    db.app = app
    models.db.create_all() 
    db.session.commit() 


#flask storage
messages = []
clients = {}
running = []

@app.route('/')
def start():
    if len(running) == 0:
        running.append("running")
        msgs=models.Messages.query.all()
        
        for msg in msgs:
            messages.append({'user':msg.name,
                'message':msg.message,
                'timestamp':msg.time,
            })
    return flask.render_template('index.html')

#user connects
@socketio.on('connect')
def on_connect():
    return socketio.emit('connected', {
        'test': 'Connected'
    })

#user disconects
@socketio.on('disconnect')
def on_disconnect():
    for sid in clients:
        clients[sid]['online']= False
    
    return socketio.emit('who is here',
        broadcast=True)
        
    
    
#user verfies presence and sends SID
@socketio.on('i am here')
def on_rollcall(clientId):
    print(clientId)
    if clientId not in clients:
        clients[clientId]={'name':'Guest',
            'online':False,
            'email':'unknown',
            'pic':'https://www.ibts.org/wp-content/uploads/2017/08/iStock-476085198.jpg',
        }
        print('Someone connected-->' + str(clients))
        
    elif clients[clientId]['email']!='unknown':
        clients[clientId]['online']=True;
    else:
        clients[clientId]['online']=False;
        
    return socketio.emit('current userlist',
        clients,
        broadcast=True
    )
#user sends message
@socketio.on('send message')
def on_send_message(data):
    date=datetime.now(TIME_ZONE)
    print("we're in")
    msg = msgParser.parsePicturesAndLinks(data['message'])
    
    #add message to db
    db.session.add(models.Messages(clients[data['id']]['name'],msg,date.strftime("%H:%M %m/%d/%y")))
    db.session.commit()
    
    #add message to this instance's data storage
    messages.append({
        'user':clients[data['id']]['name'],
        'message':msg,
        'timestamp':date.strftime("%H:%M %m/%d/%y")
    })
    
    #Check if message is a command
    if data['message'][:2] == '!!':
        #respond with bot
        data['user']='Bobby Bot'
        data['message']=bot(data['message'])
        #add bot message to db
        db.session.add(models.Messages(data['user'],data['message'],date.strftime("%H:%M %m/%d/%y")))
        db.session.commit()
        #add bot message to this instance's data storage
        messages.append({
            'user':data['user'],
            'message':data['message'],
            'timestamp':date.strftime("%H:%M %m/%d/%y")
        })
        
    #send all messages in storage to all users
    return socketio.emit('messages updated', {
        'messages': messages
    }, broadcast=True)


# listen if a new user asks for messages
@socketio.on('get messages')
def on_get_messages():
    socketio.emit('messages updated', {
        'messages': messages
    }, broadcast=True)

# listen if a user changes the name
@socketio.on('new google user')
def on_new_google_user(data):
    clients[data['id']]['name']=data['user']
    clients[data['id']]['email']=data['email']
    clients[data['id']]['pic']=data['pic']
    clients[data['id']]['online']=True
    
    # send an update to everyones user list
    socketio.emit('current userlist',
        clients,
        broadcast=True
    )
    
    return socketio.emit('current user',
        clients
    )

# get the current user list
@socketio.on('get userlist')
def on_get_userlist():
    return socketio.emit('current userlist',
        clients,
    )

# main
if __name__ == '__main__': 
    init_db(app)
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=False
    )
        