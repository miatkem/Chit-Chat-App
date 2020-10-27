import unittest
import mock

import sys, os
sys.path.append('../')

import models
import flask
from app import app, socketio
from app import db
import flask_socketio
import flask_sqlalchemy
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

import os


class mocked_unit_test(unittest.TestCase):
        
    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    def test_connect_disconnect(self):
        client = socketio.test_client(app)
        self.assertTrue(client.is_connected())
        response = client.get_received()
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['args'][0]['test'], 'Connected')
        
        EXPECTED = {
            EXPECTED_NAME: DEFAULT_NAME, 
            EXPECTED_ONLINE: False, 
            EXPECTED_EMAIL: DEFAULT_EMAIL, 
            EXPECTED_PICTURE: DEFAULT_PICTURE}
            
        client.emit('i am here', client.sid)
        response = client.get_received()
        self.assertEqual(response[0]['args'][0][client.sid], EXPECTED)
        
        
        client2 = socketio.test_client(app)
        self.assertTrue(client2.is_connected())
        client2.get_received()
        
        EXPECTED = {
            EXPECTED_NAME: DEFAULT_NAME, 
            EXPECTED_ONLINE: False, 
            EXPECTED_EMAIL: DEFAULT_EMAIL, 
            EXPECTED_PICTURE: DEFAULT_PICTURE,
        }
        
        client2.emit('i am here', client2.sid)
        response = client2.get_received()
        self.assertEqual(response[0]['args'][0][client.sid], EXPECTED)
        
        client.disconnect()
        self.assertFalse(client.is_connected())
        self.assertTrue(client2.is_connected())
        client2.disconnect()
        self.assertFalse(client2.is_connected())
  
    def test_add_google_user(self):
        client = socketio.test_client(app)
        client.get_received()
        client.emit('i am here', client.sid)
        client.get_received()
        
        NEW_USER = {
            EXPECTED_ID: client.sid,
            EXPECTED_USER: 'google_user', 
            EXPECTED_EMAIL: 'gu@gmail.com', 
            EXPECTED_PICTURE: 'testpic.png',
        }
        
        EXPECTED = [{EXPECTED_COMMAND: 'current userlist', 
        'args': [{client.sid: 
            {EXPECTED_NAME: NEW_USER[EXPECTED_USER], 
            EXPECTED_ONLINE: True, 
            EXPECTED_EMAIL: NEW_USER[EXPECTED_EMAIL], 
            EXPECTED_PICTURE: NEW_USER[EXPECTED_PICTURE]}}], 
        EXPECTED_NAMESPACE:DEFAULT_NAMESPACE},
        {EXPECTED_COMMAND: 'current user', 
        'args': [{client.sid: 
            {EXPECTED_NAME: NEW_USER[EXPECTED_USER], 
            EXPECTED_ONLINE: True, 
            EXPECTED_EMAIL: NEW_USER[EXPECTED_EMAIL], 
            EXPECTED_PICTURE: NEW_USER[EXPECTED_PICTURE]}}], 
        EXPECTED_NAMESPACE:DEFAULT_NAMESPACE}]
        
        client.emit('new google user', NEW_USER)
        
        response = client.get_received()
        
        self.assertEqual(response[0], EXPECTED[0])
        self.assertEqual(response[1], EXPECTED[1])
        
        client.emit('get userlist')
        response = client.get_received()
        self.assertEqual(len(response),1)
        print(client.sid)
        client.disconnect()
        self.assertFalse(client.is_connected())
    
    """
    def test_send_message(self):
        client = socketio.test_client(app)
        response = client.get_received()
        
        client.emit('i am here', client.sid)
        response = client.get_received()
        
        
        MESSAGE = {'message': 'This is a simple test message',
            'id' : client.sid,
        }
        
        MOCKED_MESSAGES = {
            
        }
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        

        db.create_all() 
        db.session.commit()
        db.Messages.query.all()
           
        client.emit('send message', MESSAGE)
        response = client.get_received()
        
        print(response)
        print(client.sid)
        
        
        client.emit('send message', MESSAGE)
        response = client.get_received()
        print(response)


   # def test_socketio(self):
    #    flask_test_client = app.test_client()
     #   socketio_test_client = socketio.test_client(app, flask_test_client=flask_test_client)
      #  
      #  assert socketio_test_client.is_connected()
      #  
      #  r = flask_test_client.on('connect')
      #  print(r.status_code)
      #  assert r.status_code == 200
    """
if __name__ == '__main__':
    unittest.main()