"""TESTING APP.PY WITH MOCKS"""
import unittest
import mock
import sys, os
sys.path.append('../')
import flask
from app import app, socketio, models
from app import db, on_connect, on_disconnect, on_rollcall, on_get_userlist
from app import on_new_google_user, on_get_messages, on_send_message, start
import flask_socketio
import flask_sqlalchemy
from datetime import datetime
from pytz import timezone
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

PICTURE = 'pic'
EMAIL = 'email'
ONLINE = 'online'
NAME = 'name'
USER = 'user'
COMMAND = 'name'
NAMESPACE = 'namespace'
ID = 'id'
MESSAGE = 'message'
MESSAGES = 'messages'
TIMESTAMP = 'timestamp'
RESPONSE = 'response'
DATA = 'data'
BROADCAST = 'broadcast'

DEFAULT_NAME = 'Guest'
DEFAULT_EMAIL = 'unknown'
DEFAULT_PICTURE = "https://www.ibts.org/wp-content/uploads/2017/08/iStock-476085198.jpg"
DEFAULT_NAMESPACE = '/'
TIME_ZONE = timezone('US/Eastern')

TESTCLIENTS = {
    "001": {
        NAME: DEFAULT_NAME,
        ONLINE: False,
        EMAIL: DEFAULT_EMAIL,
        PICTURE: DEFAULT_PICTURE,
    },
    "002": {
        NAME: DEFAULT_NAME,
        ONLINE: False,
        EMAIL: DEFAULT_EMAIL,
        PICTURE: DEFAULT_PICTURE,
    },
    "003": {
        NAME: 'Madison',
        ONLINE: True,
        EMAIL: 'mdm56@njit.edu',
        PICTURE: 'pictureofme.png',
    },
    "004": {
        NAME: 'Jimmy',
        ONLINE: True,
        EMAIL: 'jj56@njit.edu',
        PICTURE: 'pictureofme.png',
    }
}

TESTMESSAGES = [{
        USER:'Madison',
        MESSAGE:'This is a test message',
        TIMESTAMP:'12:12 10/26/2020',
    },
    {
        USER:'Jimmy',
        MESSAGE:'Hi ',
        TIMESTAMP:'12:14 10/26/2020',
    },
    {
        USER:'Madison',
        MESSAGE:'Hello ',
        TIMESTAMP:'12:15 10/26/2020',
    },
]

def mock_emit(response, data={}, broadcast=False):
    """mock the socketio emit function"""
    ret = {RESPONSE: response,
        DATA: data,
        BROADCAST:broadcast,
    }
    return ret


def fill_mock_db(MOCKSESSION):
    """fill the mock db with default messages"""
    for msg in TESTMESSAGES:
        MOCKSESSION.add(models.Messages(msg[USER],msg[MESSAGE],msg[TIMESTAMP]))

def mock_render(html):
    """mock the render template function"""
    return "Successfully rendered " + html


class mocked_unit_test(unittest.TestCase):
    """Mock Unit Test Class for testing app.py"""
    def setUp(self):
        """set up"""
        self.maxDiff=None

    def tearDown(self):
        """tear down"""
        pass

    def test_connect(self):
        """test connect funtion"""
        MOCKCLIENTS = TESTCLIENTS.copy()
        EXPECTEDCLIENTS = {
            "001":MOCKCLIENTS["001"],
            "002":MOCKCLIENTS["002"],
            "003":MOCKCLIENTS["003"],
            "004":MOCKCLIENTS["004"],
            "005": {
                NAME: DEFAULT_NAME,
                ONLINE: False,
                EMAIL: DEFAULT_EMAIL,
                PICTURE: DEFAULT_PICTURE,
            }
        }

        mock_clientID = '005'
        with mock.patch("app.socketio.emit", mock_emit):
            with mock.patch("app.clients", MOCKCLIENTS):
                response = on_connect()
                self.assertTrue(response[RESPONSE] == 'connected')
                response = on_rollcall(mock_clientID)
                self.assertEqual(response[DATA], EXPECTEDCLIENTS)

    def test_disconnect(self):
        """test disconnect function"""
        MOCKCLIENTS = TESTCLIENTS.copy()
        with mock.patch("app.socketio.emit", mock_emit):
            with mock.patch("app.clients", MOCKCLIENTS):

                response = on_disconnect()
                self.assertTrue(response[RESPONSE] == 'who is here')
                self.assertEqual(MOCKCLIENTS["003"]["online"], False)
                self.assertEqual(MOCKCLIENTS["004"]["online"], False)

                on_rollcall('001')
                on_rollcall('004')
                response = on_rollcall('002')

                self.assertTrue(response[RESPONSE] == 'current userlist')

                self.assertEqual(MOCKCLIENTS["003"]["online"], False)
                self.assertEqual(MOCKCLIENTS["004"]["online"], True)

    def test_get_userlist(self):
        """test get userlist function"""
        MOCKCLIENTS = TESTCLIENTS.copy()
        with mock.patch("app.socketio.emit", mock_emit):
            with mock.patch("app.clients", MOCKCLIENTS):
                response = on_get_userlist()
                self.assertTrue(response[RESPONSE] == 'current userlist')
                self.assertEqual(MOCKCLIENTS,TESTCLIENTS)

    def test_new_google_user(self):
        """test new google user function"""
        MOCKCLIENTS = TESTCLIENTS.copy()
        GOOGLEUSER = {
            ID:'001',
            USER: 'Timmy',
            EMAIL: 'tt56@njit.edu',
            PICTURE: 'profpic.jpg',
            ONLINE: True
        }
        EXPECTEDCLIENTS = {
            "001": {
                NAME: GOOGLEUSER[USER],
                ONLINE: GOOGLEUSER[ONLINE],
                EMAIL: GOOGLEUSER[EMAIL],
                PICTURE: GOOGLEUSER[PICTURE],
            },
            "002":MOCKCLIENTS["002"],
            "003":MOCKCLIENTS["003"],
            "004":MOCKCLIENTS["004"],
        }

        with mock.patch("app.socketio.emit", mock_emit):
            with mock.patch("app.clients", MOCKCLIENTS):
                response = on_new_google_user(GOOGLEUSER)
                self.assertTrue(response[RESPONSE] == 'current user')
                self.assertEqual(response[DATA],EXPECTEDCLIENTS)

    def test_getMessages(self):
        """test get messages function"""
        MOCKCLIENTS = TESTCLIENTS.copy()
        MOCKMESSAGES = TESTMESSAGES.copy()
        EXPECTEDMESSAGES = TESTMESSAGES.copy()
        with mock.patch("app.socketio.emit", mock_emit):
            with mock.patch("app.clients", MOCKCLIENTS):
                with mock.patch("app.messages", MOCKMESSAGES):
                    response = on_get_messages()
                    self.assertTrue(response[RESPONSE] == 'messages updated')
                    self.assertEqual(response[DATA][MESSAGES], EXPECTEDMESSAGES)

    def test_send_normal_messages(self):
        """test sending normal messages"""
        MOCKCLIENTS = TESTCLIENTS.copy()
        MOCKMESSAGES = TESTMESSAGES.copy()
        MOCKSESSION = UnifiedAlchemyMagicMock()

        TESTMESSAGE = {
            USER:'Madison',
            ID:'003',
            MESSAGE:'Mock testing is awesome',
        }

        EXPECTEDMESSAGES = [
            MOCKMESSAGES[0],
            MOCKMESSAGES[1],
            MOCKMESSAGES[2],
            {
                USER:'Madison',
                MESSAGE:'Mock testing is awesome ',
                TIMESTAMP: datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
            }
        ]

        with mock.patch("app.socketio.emit", mock_emit):
            with mock.patch("app.clients", MOCKCLIENTS):
                with mock.patch("app.messages", MOCKMESSAGES):
                    with mock.patch("app.db.session", MOCKSESSION):
                        fill_mock_db(MOCKSESSION)
                        response =on_send_message(TESTMESSAGE)
                        self.assertTrue(response[RESPONSE] == 'messages updated')
                        self.assertEqual(response[DATA][MESSAGES], EXPECTEDMESSAGES)
                        MOCKDB = MOCKSESSION.query(models.Messages).all()
                        for i in range(0,len(MOCKDB)):
                            self.assertEqual(MOCKDB[i].name, EXPECTEDMESSAGES[i][USER])
                            self.assertEqual(MOCKDB[i].message, EXPECTEDMESSAGES[i][MESSAGE])
                            self.assertEqual(MOCKDB[i].time, EXPECTEDMESSAGES[i][TIMESTAMP])

    def test_sendImageMessages(self):
        """test sending image messages"""
        MOCKCLIENTS = TESTCLIENTS.copy()
        MOCKMESSAGES = TESTMESSAGES.copy()
        MOCKSESSION = UnifiedAlchemyMagicMock()
        TESTMESSAGE = {
            USER:'Madison',
            ID:'003',
            MESSAGE:('This is an image https://upload.wikimedia.org/wikipedia/commons/'+
            'thumb/3/3e/Tokyo_Sky_Tree_2012.JPG/220px-Tokyo_Sky_Tree_2012.jpg'),
        }
        EXPECTEDMESSAGES = [
            MOCKMESSAGES[0],
            MOCKMESSAGES[1],
            MOCKMESSAGES[2],
            {
                USER:'Madison',
                MESSAGE:("This is an image <img src='https://upload.wikimedia.org/wikipedia/"+
                "commons/thumb/3/3e/Tokyo_Sky_Tree_2012.JPG/220px-Tokyo_Sky_Tree_2012.jpg'"+
                " class='msgImg'/> "),
                TIMESTAMP: datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
            }
        ]

        with mock.patch("app.socketio.emit", mock_emit):
            with mock.patch("app.clients", MOCKCLIENTS):
                with mock.patch("app.messages", MOCKMESSAGES):
                    with mock.patch("app.db.session", MOCKSESSION):
                        fill_mock_db(MOCKSESSION)
                        response =on_send_message(TESTMESSAGE)
                        self.assertTrue(response[RESPONSE] == 'messages updated')
                        self.assertEqual(response[DATA][MESSAGES], EXPECTEDMESSAGES)
                        MOCKDB = MOCKSESSION.query(models.Messages).all()
                        for i in range(0,len(MOCKDB)):
                            self.assertEqual(MOCKDB[i].name, EXPECTEDMESSAGES[i][USER])
                            self.assertEqual(MOCKDB[i].message, EXPECTEDMESSAGES[i][MESSAGE])
                            self.assertEqual(MOCKDB[i].time, EXPECTEDMESSAGES[i][TIMESTAMP])

    def test_send_link_messages(self):
        """test sending link messages"""
        MOCKCLIENTS = TESTCLIENTS.copy()
        MOCKMESSAGES = TESTMESSAGES.copy()
        MOCKSESSION = UnifiedAlchemyMagicMock()
        TESTMESSAGE = {
            USER:'Madison',
            ID:'003',
            MESSAGE:'This is a link https://www.google.com/',
        }
        EXPECTEDMESSAGES = [
            MOCKMESSAGES[0],
            MOCKMESSAGES[1],
            MOCKMESSAGES[2],
            {
                USER:'Madison',
                MESSAGE:("This is a link <a href='https://www.google.com/' " +
                "target='_blank'>https://www.google.com/</a> "),
                TIMESTAMP: datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
            }
        ]

        with mock.patch("app.socketio.emit", mock_emit):
            with mock.patch("app.clients", MOCKCLIENTS):
                with mock.patch("app.messages", MOCKMESSAGES):
                    with mock.patch("app.db.session", MOCKSESSION):
                        fill_mock_db(MOCKSESSION)
                        response =on_send_message(TESTMESSAGE)
                        self.assertTrue(response[RESPONSE] == 'messages updated')
                        self.assertEqual(response[DATA][MESSAGES], EXPECTEDMESSAGES)
                        MOCKDB = MOCKSESSION.query(models.Messages).all()
                        for i in range(0,len(MOCKDB)):
                            self.assertEqual(MOCKDB[i].name, EXPECTEDMESSAGES[i][USER])
                            self.assertEqual(MOCKDB[i].message, EXPECTEDMESSAGES[i][MESSAGE])
                            self.assertEqual(MOCKDB[i].time, EXPECTEDMESSAGES[i][TIMESTAMP])

    def test_send_bot_messages_with_known_results(self):
        """test sending simple bot messages"""
        BOT_COMMANDS = ['!! about', '!! help', '!! fakeCommand']
        BOT_RESPONSES = [
            ('Hi, I am BobbyBot. I am a pretty fun guy. If there is something you need from me '+
            'let me know. To find out what I am capable of type !! help'),
            ('!! about - learn about me<br>!! help - shows this screen<br>!! funtranslate '+
            '{message} - translate message to {language}<br>!! flip - flip a coin<br>!! '+
            'bitcoin - I will tell you bitcoins price'),
            "I don't know how to do that"
        ]

        for bot in range(0,len(BOT_COMMANDS)):
            MOCKCLIENTS = TESTCLIENTS.copy()
            MOCKMESSAGES = TESTMESSAGES.copy()
            MOCKSESSION = UnifiedAlchemyMagicMock()
            TESTMESSAGE = {
                USER:'Madison',
                ID:'003',
                MESSAGE:BOT_COMMANDS[bot],
            }
            EXPECTEDMESSAGES = [
                MOCKMESSAGES[0],
                MOCKMESSAGES[1],
                MOCKMESSAGES[2],
                {
                    USER:'Madison',
                    MESSAGE:BOT_COMMANDS[bot] + ' ',
                    TIMESTAMP: datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
                },
                {
                    USER:'Bobby Bot',
                    MESSAGE:BOT_RESPONSES[bot],
                    TIMESTAMP: datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
                }
            ]

            with mock.patch("app.socketio.emit", mock_emit):
                with mock.patch("app.clients", MOCKCLIENTS):
                    with mock.patch("app.messages", MOCKMESSAGES):
                        with mock.patch("app.db.session", MOCKSESSION):
                            fill_mock_db(MOCKSESSION)
                            response =on_send_message(TESTMESSAGE)
                            self.assertTrue(response[RESPONSE] == 'messages updated')
                            self.assertEqual(response[DATA][MESSAGES], EXPECTEDMESSAGES)
                            MOCKDB = MOCKSESSION.query(models.Messages).all()
                            for i in range(0,len(MOCKDB)):
                                self.assertEqual(MOCKDB[i].name, EXPECTEDMESSAGES[i][USER])
                                self.assertEqual(MOCKDB[i].message, EXPECTEDMESSAGES[i][MESSAGE])
                                self.assertEqual(MOCKDB[i].time, EXPECTEDMESSAGES[i][TIMESTAMP])

    def test_send_bot_messages_with_unknown_results(self):
        """test sending complex bot messages"""
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
                USER:'Madison',
                ID:'003',
                MESSAGE:BOT_COMMANDS[bot],
            }
            EXPECTEDMESSAGES = [[
                MOCKMESSAGES[0],
                MOCKMESSAGES[1],
                MOCKMESSAGES[2],
                {
                    USER:'Madison',
                    MESSAGE:BOT_COMMANDS[bot] + ' ',
                    TIMESTAMP: datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
                },
                {
                    USER:'Bobby Bot',
                    MESSAGE:BOT_RESPONSES[bot][0],
                    TIMESTAMP: datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
                }
            ],[
                MOCKMESSAGES[0],
                MOCKMESSAGES[1],
                MOCKMESSAGES[2],
                {
                    USER:'Madison',
                    MESSAGE:BOT_COMMANDS[bot] + ' ',
                    TIMESTAMP: datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
                },
                {
                    USER:'Bobby Bot',
                    MESSAGE:BOT_RESPONSES[bot][1],
                    TIMESTAMP: datetime.now(TIME_ZONE).strftime("%H:%M %m/%d/%y")
                }
            ]]

            with mock.patch("app.socketio.emit", mock_emit):
                with mock.patch("app.clients", MOCKCLIENTS):
                    with mock.patch("app.messages", MOCKMESSAGES):
                        with mock.patch("app.db.session", MOCKSESSION):
                            fill_mock_db(MOCKSESSION)
                            response =on_send_message(TESTMESSAGE)
                            self.assertTrue(response[RESPONSE] == 'messages updated')
                            self.assertTrue((response[DATA][MESSAGES] == EXPECTEDMESSAGES[0]) 
                                or (response[DATA][MESSAGES] == EXPECTEDMESSAGES[1]))
                            MOCKDB = MOCKSESSION.query(models.Messages).all()
                            for i in range(0,len(MOCKDB)):
                                self.assertEqual(MOCKDB[i].name, EXPECTEDMESSAGES[0][i][USER])
                                self.assertTrue((MOCKDB[i].message==EXPECTEDMESSAGES[0][i][MESSAGE]
                                    or MOCKDB[i].message==EXPECTEDMESSAGES[1][i][MESSAGE]))
                                self.assertEqual(MOCKDB[i].time, EXPECTEDMESSAGES[0][i][TIMESTAMP])

    def test_start(self):
        """test start function"""
        MOCKSESSION = UnifiedAlchemyMagicMock()
        with mock.patch("app.db.session", MOCKSESSION):
            with mock.patch("flask.render_template", mock_render):
                response = start()
                self.assertEqual(response, "Successfully rendered index.html")

if __name__ == '__main__':
    unittest.main()
