import unittest
import mock

import sys, os
sys.path.append('../')

import flask
from app import app, socketio, models
from app import db, on_connect, on_disconnect, on_rollcall, on_get_userlist, on_new_google_user, on_get_messages, on_send_message, start
import flask_socketio
import flask_sqlalchemy
from datetime import datetime
from pytz import timezone
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

EXPECTED_PICTURE = 'pic'
EXPECTED_EMAIL = 'email'
EXPECTED_ONLINE = 'online'
EXPECTED_NAME = 'name'
EXPECTED_USER = 'user'
EXPECTED_COMMAND = 'name'
EXPECTED_NAMESPACE = 'namespace'
EXPECTED_ID = 'id'

DEFAULT_NAME = 'Guest'
DEFAULT_EMAIL = 'unknown'
DEFAULT_PICTURE = "https://www.ibts.org/wp-content/uploads/2017/08/iStock-476085198.jpg"
DEFAULT_NAMESPACE = '/'
TIME_ZONE = timezone('US/Eastern');

import os


def mockEmit(response, data={}, broadcast=False):
    ret = {'response': response,
        'data': data,
        'broadcast':broadcast,
    }
    
    return ret
    
def fillMockDB(MOCKSESSION):
    for msg in TESTMESSAGES:
        MOCKSESSION.add(models.Messages(msg['user'],msg['message'],msg['timestamp']))
        
def mockRender(html):
    return "Successfully rendered " + html
    
        

TESTCLIENTS = {
    "001": {
        'name': DEFAULT_NAME,
        'online': False,
        'email': DEFAULT_EMAIL,
        'pic': DEFAULT_PICTURE,
    },
    "002": {
        'name': DEFAULT_NAME,
        'online': False,
        'email': DEFAULT_EMAIL,
        'pic': DEFAULT_PICTURE,
    },
    "003": {
        'name': 'Madison',
        'online': True,
        'email': 'mdm56@njit.edu',
        'pic': 'pictureofme.png',
    },
    "004": {
        'name': 'Jimmy',
        'online': True,
        'email': 'jj56@njit.edu',
        'pic': 'pictureofme.png',
    }
    
}

TESTMESSAGES = [{
        'user':'Madison',
        'message':'This is a test message',
        'timestamp':'12:12 10/26/2020',
    },
    {
        'user':'Jimmy',
        'message':'Hi ',
        'timestamp':'12:14 10/26/2020',
    },
    {
        'user':'Madison',
        'message':'Hello ',
        'timestamp':'12:15 10/26/2020',
    },
]


class mocked_unit_test(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff=None

    def tearDown(self):
        pass
    
        
    def test_connect(self):
        MOCKCLIENTS = TESTCLIENTS.copy()
        EXPECTEDCLIENTS = {
            "001":MOCKCLIENTS["001"],
            "002":MOCKCLIENTS["002"],
            "003":MOCKCLIENTS["003"],
            "004":MOCKCLIENTS["004"],
            "005": {
                'name': DEFAULT_NAME,
                'online': False,
                'email': DEFAULT_EMAIL,
                'pic': DEFAULT_PICTURE,
            }
            
        }

        
        mock_clientID = '005'
        with mock.patch("app.socketio.emit", mockEmit):
            with mock.patch("app.clients", MOCKCLIENTS):
                response = on_connect()
                self.assertTrue(response['response'] == 'connected')
                response = on_rollcall(mock_clientID)
                self.assertEquals(response['data'], EXPECTEDCLIENTS)
                
        print("TEST1=>" + str(MOCKCLIENTS))
        
        
                
    def test_disconnect(self):
        MOCKCLIENTS = TESTCLIENTS.copy()
        with mock.patch("app.socketio.emit", mockEmit):
            with mock.patch("app.clients", MOCKCLIENTS):
              
                response = on_disconnect()
                self.assertTrue(response['response'] == 'who is here')
                
                self.assertEqual(MOCKCLIENTS["003"]["online"], False)
                self.assertEqual(MOCKCLIENTS["004"]["online"], False)
                
                on_rollcall('001')
                on_rollcall('004')
                response = on_rollcall('002')
    
                self.assertTrue(response['response'] == 'current userlist')
                
                self.assertEqual(MOCKCLIENTS["003"]["online"], False)
                self.assertEqual(MOCKCLIENTS["004"]["online"], True)
                print("TEST2=>" + str(MOCKCLIENTS))
    
    def test_getUserlist(self):
        MOCKCLIENTS = TESTCLIENTS.copy()
        with mock.patch("app.socketio.emit", mockEmit):
            with mock.patch("app.clients", MOCKCLIENTS):
                response = on_get_userlist()
                self.assertTrue(response['response'] == 'current userlist')
                self.assertEqual(MOCKCLIENTS,TESTCLIENTS)
                
    def test_newGoogleUser(self):
        MOCKCLIENTS = TESTCLIENTS.copy()
        GOOGLEUSER = {
            'id':'001',
            'user': 'Timmy',
            'email': 'tt56@njit.edu',
            'pic': 'profpic.jpg',
            'online': True
        }
        EXPECTEDCLIENTS = {
            "001": {
                'name': GOOGLEUSER['user'],
                'online': GOOGLEUSER['online'],
                'email': GOOGLEUSER['email'],
                'pic': GOOGLEUSER['pic'],    
            },
            "002":MOCKCLIENTS["002"],
            "003":MOCKCLIENTS["003"],
            "004":MOCKCLIENTS["004"],
        }
        
        with mock.patch("app.socketio.emit", mockEmit):
            with mock.patch("app.clients", MOCKCLIENTS):
                response = on_new_google_user(GOOGLEUSER)
                self.assertTrue(response['response'] == 'current user')
                print(response['data'],EXPECTEDCLIENTS)
                self.assertEqual(response['data'],EXPECTEDCLIENTS)
    
    def test_getMessages(self):
        MOCKCLIENTS = TESTCLIENTS.copy()
        MOCKMESSAGES = TESTMESSAGES.copy()
        EXPECTEDMESSAGES = TESTMESSAGES.copy()
        with mock.patch("app.socketio.emit", mockEmit):
            with mock.patch("app.clients", MOCKCLIENTS):
                with mock.patch("app.messages", MOCKMESSAGES):
                    response = on_get_messages()
                    self.assertTrue(response['response'] == 'messages updated')
                    self.assertEqual(response['data']['messages'], EXPECTEDMESSAGES)
    
    def test_sendNormalMessages(self):
        MOCKCLIENTS = TESTCLIENTS.copy()
        MOCKMESSAGES = TESTMESSAGES.copy()
        
        MOCKSESSION = UnifiedAlchemyMagicMock()
        
        TESTMESSAGE = {
            'user':'Madison',
            'id':'003',
            'message':'Mock testing is awesome',
        }
    
        
        EXPECTEDMESSAGES = [
            MOCKMESSAGES[0],
            MOCKMESSAGES[1],
            MOCKMESSAGES[2],
            {
                'user':'Madison',
                'message':'Mock testing is awesome ',
                'timestamp': datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
            }
        ]
                        
        
        with mock.patch("app.socketio.emit", mockEmit):
            with mock.patch("app.clients", MOCKCLIENTS):
                with mock.patch("app.messages", MOCKMESSAGES):
                    with mock.patch("app.db.session", MOCKSESSION):
                        fillMockDB(MOCKSESSION)
                        response =on_send_message(TESTMESSAGE)
                        self.assertTrue(response['response'] == 'messages updated')
                        print(response['data']['messages'])
                        self.assertEqual(response['data']['messages'], EXPECTEDMESSAGES)
                        MOCKDB = MOCKSESSION.query(models.Messages).all()
                        #self.assertEqual(MOCKDB, EXPECTEDMESSAGES)
                        print(MOCKDB)
                        for i in range(0,len(MOCKDB)):
                            self.assertEqual(MOCKDB[i].name, EXPECTEDMESSAGES[i]['user'])
                            self.assertEqual(MOCKDB[i].message, EXPECTEDMESSAGES[i]['message'])
                            self.assertEqual(MOCKDB[i].time, EXPECTEDMESSAGES[i]['timestamp'])
                            
    def test_sendImageMessages(self):
        MOCKCLIENTS = TESTCLIENTS.copy()
        MOCKMESSAGES = TESTMESSAGES.copy()
        MOCKSESSION = UnifiedAlchemyMagicMock()
        TESTMESSAGE = {
            'user':'Madison',
            'id':'003',
            'message':'This is an image https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Tokyo_Sky_Tree_2012.JPG/220px-Tokyo_Sky_Tree_2012.jpg',
        }
        EXPECTEDMESSAGES = [
            MOCKMESSAGES[0],
            MOCKMESSAGES[1],
            MOCKMESSAGES[2],
            {
                'user':'Madison',
                'message':"This is an image <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Tokyo_Sky_Tree_2012.JPG/220px-Tokyo_Sky_Tree_2012.jpg' class='msgImg'/> ",
                'timestamp': datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
            }
        ]
        
        with mock.patch("app.socketio.emit", mockEmit):
            with mock.patch("app.clients", MOCKCLIENTS):
                with mock.patch("app.messages", MOCKMESSAGES):
                    with mock.patch("app.db.session", MOCKSESSION):
                        fillMockDB(MOCKSESSION)
                        response =on_send_message(TESTMESSAGE)
                        self.assertTrue(response['response'] == 'messages updated')
                        print(response['data']['messages'])
                        self.assertEqual(response['data']['messages'], EXPECTEDMESSAGES)
                        MOCKDB = MOCKSESSION.query(models.Messages).all()
                        #self.assertEqual(MOCKDB, EXPECTEDMESSAGES)
                        for i in range(0,len(MOCKDB)):
                            self.assertEqual(MOCKDB[i].name, EXPECTEDMESSAGES[i]['user'])
                            self.assertEqual(MOCKDB[i].message, EXPECTEDMESSAGES[i]['message'])
                            self.assertEqual(MOCKDB[i].time, EXPECTEDMESSAGES[i]['timestamp'])
    
    def test_sendLinkMessages(self):
        MOCKCLIENTS = TESTCLIENTS.copy()
        MOCKMESSAGES = TESTMESSAGES.copy()
        MOCKSESSION = UnifiedAlchemyMagicMock()
        TESTMESSAGE = {
            'user':'Madison',
            'id':'003',
            'message':'This is a link https://www.google.com/',
        }
        EXPECTEDMESSAGES = [
            MOCKMESSAGES[0],
            MOCKMESSAGES[1],
            MOCKMESSAGES[2],
            {
                'user':'Madison',
                'message':"This is a link <a href='https://www.google.com/' target='_blank'>https://www.google.com/</a> ",
                'timestamp': datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
            }
        ]
        
        with mock.patch("app.socketio.emit", mockEmit):
            with mock.patch("app.clients", MOCKCLIENTS):
                with mock.patch("app.messages", MOCKMESSAGES):
                    with mock.patch("app.db.session", MOCKSESSION):
                        fillMockDB(MOCKSESSION)
                        response =on_send_message(TESTMESSAGE)
                        self.assertTrue(response['response'] == 'messages updated')
                        print(response['data']['messages'])
                        self.assertEqual(response['data']['messages'], EXPECTEDMESSAGES)
                        MOCKDB = MOCKSESSION.query(models.Messages).all()
                        #self.assertEqual(MOCKDB, EXPECTEDMESSAGES)
                        for i in range(0,len(MOCKDB)):
                            self.assertEqual(MOCKDB[i].name, EXPECTEDMESSAGES[i]['user'])
                            self.assertEqual(MOCKDB[i].message, EXPECTEDMESSAGES[i]['message'])
                            self.assertEqual(MOCKDB[i].time, EXPECTEDMESSAGES[i]['timestamp'])
    
    def test_sendBotMessagesWithKnownResults(self):
        BOT_COMMANDS = ['!! about', '!! help', '!! fakeCommand']
        BOT_RESPONSES = [
            'Hi, I am BobbyBot. I am a pretty fun guy. If there is something you need from me let me know. To find out what I am capable of type !! help',
            '!! about - learn about me<br>!! help - shows this screen<br>!! funtranslate {message} - translate message to {language}<br>!! flip - flip a coin<br>!! bitcoin - I will tell you bitcoins price',
            "I don't know how to do that"
        ]
        
        for bot in range(0,len(BOT_COMMANDS)):
        
            MOCKCLIENTS = TESTCLIENTS.copy()
            MOCKMESSAGES = TESTMESSAGES.copy()
            MOCKSESSION = UnifiedAlchemyMagicMock()
            TESTMESSAGE = {
                'user':'Madison',
                'id':'003',
                'message':BOT_COMMANDS[bot],
            }
            EXPECTEDMESSAGES = [
                MOCKMESSAGES[0],
                MOCKMESSAGES[1],
                MOCKMESSAGES[2],
                {
                    'user':'Madison',
                    'message':BOT_COMMANDS[bot] + ' ',
                    'timestamp': datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
                },
                {
                    'user':'Bobby Bot',
                    'message':BOT_RESPONSES[bot],
                    'timestamp': datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
                }
            ]
            
            with mock.patch("app.socketio.emit", mockEmit):
                with mock.patch("app.clients", MOCKCLIENTS):
                    with mock.patch("app.messages", MOCKMESSAGES):
                        with mock.patch("app.db.session", MOCKSESSION):
                            fillMockDB(MOCKSESSION)
                            response =on_send_message(TESTMESSAGE)
                            self.assertTrue(response['response'] == 'messages updated')
                            print(response['data']['messages'])
                            self.assertEqual(response['data']['messages'], EXPECTEDMESSAGES)
                            MOCKDB = MOCKSESSION.query(models.Messages).all()
                            #self.assertEqual(MOCKDB, EXPECTEDMESSAGES)
                            for i in range(0,len(MOCKDB)):
                                self.assertEqual(MOCKDB[i].name, EXPECTEDMESSAGES[i]['user'])
                                self.assertEqual(MOCKDB[i].message, EXPECTEDMESSAGES[i]['message'])
                                self.assertEqual(MOCKDB[i].time, EXPECTEDMESSAGES[i]['timestamp'])
    
    def test_sendBotMessagesWithUnknownResults(self):
        BOT_COMMANDS = ['!! flip', '!! funtranslate I like apples.']
        BOT_RESPONSES = [
            [
               'The coin landed HEADS up', 
               'The coin landed TAILS up'
            ],
            [
                'I-way ike-lay apples-way.',
                'Sorry the limit for translations has been reached'
                
            ]
        ]
        
        for bot in range(0,len(BOT_COMMANDS)):
        
            MOCKCLIENTS = TESTCLIENTS.copy()
            MOCKMESSAGES = TESTMESSAGES.copy()
            MOCKSESSION = UnifiedAlchemyMagicMock()
            TESTMESSAGE = {
                'user':'Madison',
                'id':'003',
                'message':BOT_COMMANDS[bot],
            }
            EXPECTEDMESSAGES = [[
                MOCKMESSAGES[0],
                MOCKMESSAGES[1],
                MOCKMESSAGES[2],
                {
                    'user':'Madison',
                    'message':BOT_COMMANDS[bot] + ' ',
                    'timestamp': datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
                },
                {
                    'user':'Bobby Bot',
                    'message':BOT_RESPONSES[bot][0],
                    'timestamp': datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
                }
            ],[
                MOCKMESSAGES[0],
                MOCKMESSAGES[1],
                MOCKMESSAGES[2],
                {
                    'user':'Madison',
                    'message':BOT_COMMANDS[bot] + ' ',
                    'timestamp': datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
                },
                {
                    'user':'Bobby Bot',
                    'message':BOT_RESPONSES[bot][1],
                    'timestamp': datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
                }
            ]]
            
            with mock.patch("app.socketio.emit", mockEmit):
                with mock.patch("app.clients", MOCKCLIENTS):
                    with mock.patch("app.messages", MOCKMESSAGES):
                        with mock.patch("app.db.session", MOCKSESSION):
                            fillMockDB(MOCKSESSION)
                            response =on_send_message(TESTMESSAGE)
                            self.assertTrue(response['response'] == 'messages updated')
                            print(response['data']['messages'])
                            self.assertTrue((response['data']['messages'] == EXPECTEDMESSAGES[0]) or (response['data']['messages'] == EXPECTEDMESSAGES[1]))
                            MOCKDB = MOCKSESSION.query(models.Messages).all()
                            #self.assertEqual(MOCKDB, EXPECTEDMESSAGES)
                            for i in range(0,len(MOCKDB)):
                                self.assertEqual(MOCKDB[i].name, EXPECTEDMESSAGES[0][i]['user'])
                                self.assertTrue(MOCKDB[i].message==EXPECTEDMESSAGES[0][i]['message'] 
                                    or MOCKDB[i].message==EXPECTEDMESSAGES[1][i]['message'])
                                self.assertEqual(MOCKDB[i].time, EXPECTEDMESSAGES[0][i]['timestamp'])
                                
    def test_start(self):
        MOCKSESSION = UnifiedAlchemyMagicMock()
        with mock.patch("app.db.session", MOCKSESSION):
            with mock.patch("flask.render_template", mockRender):
                response = start()
                self.assertEqual(response, "Successfully rendered index.html")
                
            
if __name__ == '__main__':
    unittest.main()