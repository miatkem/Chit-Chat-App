import os
import flask
import flask_socketio
import flask_sqlalchemy
import random
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
import requests
import models

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

#

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app
db.create_all()
db.session.commit()


#flask storage
messages = []
clients = {}

@app.route('/')
def start():
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
    socketio.emit('connected', {
        'test': 'Connected'
    })

#user disconects
@socketio.on('disconnect')
def on_disconnect():
    for sid in clients:
        clients[sid]['online']= False
        
    socketio.emit('who is here',
        broadcast=True)
        
    print('Someone disconnected-->' + str(clients))
    
    
    
#user verfies presence and sends SID
@socketio.on('i am here')
def on_arrive(clientId):
    if clientId not in clients:
        clients[clientId]={'name':'Guest',
            'online':True
        }
        print('Someone connected-->' + str(clients))
    else:
        clients[clientId]['online'] = True
    
    socketio.emit('current userlist',
        clients,
        broadcast=True
    )
#user sends message
@socketio.on('send message')
def on_send_message(data):
    date=datetime.now(TIME_ZONE)
    
    #add message to db
    db.session.add(models.Messages(clients[data['id']]['name'],data['message'],date.strftime("%H:%M %m/%d/%y")))
    db.session.commit()
    
    #add message to this instance's data storage
    messages.append({
        'user':clients[data['id']]['name'],
        'message':data['message'],
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
            'timestamp':data['timestamp']
        })
        
    #send all messages in storage to all users
    socketio.emit('messages updated', {
        'messages': messages
    }, broadcast=True)

#based on command respond with bot
def bot(message):
    spltmsg = message.split()
    cmd = spltmsg[1]
    if cmd == 'about': # description of bot
        return 'Hi, I am BobbyBot. I am a pretty fun guy. If there is something you need from me let me know. To find out what I am capable of typ !! help'
    elif cmd == 'help': # command list
        ret = "!! about - learn about me<br>"
        ret += "!! help - shows this screen<br>"
        ret += "!! funtranslate {message} - translate message to {language}<br>"
        ret += "!! flip - flip a coin<br>"
        ret += "!! bitcoin - I will tell you bitcoins price"
        return ret
    elif cmd == 'flip': # flip a coin
        coin = random.getrandbits(1)
        if coin == 1:
            return 'The coin landed HEADS up'
        else:
            return 'The coin landed TAILS up'
    
    elif cmd == 'funtranslate': # translate to piglatin
        url = "https://api.funtranslations.com/translate/pig-latin.json?text="
        for i in range(2,len(spltmsg)):
            url+=spltmsg[i] + '%20'
        r=requests.get(url)
        data = r.json()
        return data["contents"]["translated"]
        
    elif cmd == 'bitcoin': # message the price of bitcoin
        url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        r=requests.get(url)
        data = r.json()
        return "1 bitcoin is currently worth " + data["bpi"]["USD"]["symbol"] + "" + data["bpi"]["USD"]["rate"]
        
    else: # command doesn't exist
        return "I don't know how to do that"

# listen if a new user asks for messages
@socketio.on('get messages')
def on_get_messages():
    socketio.emit('messages updated', {
        'messages': messages
    }, broadcast=True)

# listen if a user changes the name
@socketio.on('new google user')
def on_get_name(data):
    clients[data['id']]['name']=data['user']
    print(data['user'])
    
    # send an update to everyones user list
    socketio.emit('current userlist',
        clients,
        broadcast=True
    )

# get the current user list
@socketio.on('get userlist')
def on_get_userlist():
    socketio.emit('current userlist',
        clients
    )

# main
if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=False
    )
