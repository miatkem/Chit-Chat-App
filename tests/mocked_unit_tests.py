import unittest
import mock

import sys, os
sys.path.append('../')

import models
from app import app, socketio
from app import db
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

EXPECTED_PICTURE = 'pic'
EXPECTED_EMAIL = 'email'
EXPECTED_ONLINE = 'online'
EXPECTED_NAME = 'name'
EXPECTED_COMMAND = 'name'
EXPECTED_NAMESPACE = 'namespace'

DEFAULT_NAME = 'Guest'
DEFAULT_EMAIL = 'unknown'
DEFAULT_PICTURE = "https://www.ibts.org/wp-content/uploads/2017/08/iStock-476085198.jpg"
DEFAULT_NAMESPACE = '/'


class Test_Client(unittest.TestCase):
    
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
        
        EXPECTED = [{EXPECTED_COMMAND: 'current userlist', 
        'args': [{client.sid: 
            {EXPECTED_NAME: DEFAULT_NAME, 
            EXPECTED_ONLINE: False, 
            EXPECTED_EMAIL: DEFAULT_EMAIL, 
            EXPECTED_PICTURE: DEFAULT_PICTURE}}], 
        EXPECTED_NAMESPACE:DEFAULT_NAMESPACE}]
    
        client.emit('i am here', client.sid)
        response = client.get_received()
        self.assertEqual(response, EXPECTED)
        
        
        client2 = socketio.test_client(app)
        self.assertTrue(client2.is_connected())
        client2.get_received()
        
        EXPECTED[0]['args'][0][client2.sid] = {
            EXPECTED_NAME: DEFAULT_NAME, 
            EXPECTED_ONLINE: False, 
            EXPECTED_EMAIL: DEFAULT_EMAIL, 
            EXPECTED_PICTURE: DEFAULT_PICTURE,
        }
        
        client2.emit('i am here', client2.sid)
        response = client2.get_received()
        self.assertEqual(response, EXPECTED)
        
        client.disconnect()
        self.assertFalse(client.is_connected())
        self.assertTrue(client2.is_connected())
        client2.disconnect()
        self.assertFalse(client2.is_connected())
  
        
        



   # def test_socketio(self):
    #    flask_test_client = app.test_client()
     #   socketio_test_client = socketio.test_client(app, flask_test_client=flask_test_client)
      #  
      #  assert socketio_test_client.is_connected()
      #  
      #  r = flask_test_client.on('connect')
      #  print(r.status_code)
      #  assert r.status_code == 200
        
if __name__ == '__main__':
    unittest.main()