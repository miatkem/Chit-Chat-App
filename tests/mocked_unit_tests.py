import unittest
import mock

import sys, os
sys.path.append('../')

import models
import flask
from app import app, socketio
from app import db, on_connect, on_disconnect, on_rollcall, on_get_userlist, on_new_google_user, on_get_messages
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
                    
                

if __name__ == '__main__':
    unittest.main()