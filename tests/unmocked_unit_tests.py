import unittest

from os.path import dirname, join
import sys
sys.path.insert(1, join(dirname(__file__), '../'))
from bot import bot
from msgParser import parsePicturesAndLinks

import unittest.mock as mock
from os.path import join, dirname

KEY_TYPE = "type"
KEY_INPUT = "input"
KEY_EXPECTED = "expected"

class MockedUnitTestCase(unittest.TestCase):
    def test_parsePicturesAndLinks(self):
        self.test_params = [
            {
                KEY_INPUT: "https://www.freepngimg.com/thumb/burger/22388-5-burger-food.png",
                KEY_EXPECTED: "<img src='https://www.freepngimg.com/thumb/burger/22388-5-burger-food.png' class='msgImg'/> "
            },
            {
                KEY_INPUT: "No link words and then an image -> https://www.freepngimg.com/thumb/burger/22388-5-burger-food.png",
                KEY_EXPECTED: "No link words and then an image -> <img src='https://www.freepngimg.com/thumb/burger/22388-5-burger-food.png' class='msgImg'/> "
            },
            {
                KEY_INPUT: "https://www.seriouseats.com/recipes/images/2015/07/20150702-sous-vide-hamburger-anova-primary.jpg",
                KEY_EXPECTED: "<img src='https://www.seriouseats.com/recipes/images/2015/07/20150702-sous-vide-hamburger-anova-primary.jpg' class='msgImg'/> "
            },
            {
                KEY_INPUT: "https://media4.giphy.com/media/7NXp5l8D4oRsm0XxiK/giphy.gif",
                KEY_EXPECTED: "<img src='https://media4.giphy.com/media/7NXp5l8D4oRsm0XxiK/giphy.gif' class='msgImg'/> "
            },
            {
                KEY_INPUT: "No link words and then a gif -> https://media4.giphy.com/media/7NXp5l8D4oRsm0XxiK/giphy.gif",
                KEY_EXPECTED: "No link words and then a gif -> <img src='https://media4.giphy.com/media/7NXp5l8D4oRsm0XxiK/giphy.gif' class='msgImg'/> "
            },
            {
                KEY_INPUT: "5-burger-food.png",
                KEY_EXPECTED: "5-burger-food.png "
            },
            {
                KEY_INPUT: "us-vide-hamburger-anova-primary.jpg",
                KEY_EXPECTED: "us-vide-hamburger-anova-primary.jpg "
            },
            {
                KEY_INPUT: "giphy.gif",
                KEY_EXPECTED: "giphy.gif "
            },
            {
                KEY_INPUT: "No link words and then a failed gif -> giphy.gif ",
                KEY_EXPECTED: "No link words and then a failed gif -> giphy.gif "
            },
            {
                KEY_INPUT: "https://www.google.com/",
                KEY_EXPECTED: "<a href='https://www.google.com/' target='_blank'>https://www.google.com/</a> "
            },
            {
                KEY_INPUT: "http://www.njit.edu/",
                KEY_EXPECTED: "<a href='http://www.njit.edu/' target='_blank'>http://www.njit.edu/</a> "
            },
             {
                KEY_INPUT: "No link words and then a link -> http://www.njit.edu/",
                KEY_EXPECTED: "No link words and then a link -> <a href='http://www.njit.edu/' target='_blank'>http://www.njit.edu/</a> "
            },
            {
                KEY_INPUT: "www.njit.edu/",
                KEY_EXPECTED: "www.njit.edu/ "
            },
            {
                KEY_INPUT: "No links",
                KEY_EXPECTED: "No links "
            },
            
        ]
            
            
        for test_case in self.test_params:
            response = parsePicturesAndLinks(test_case[KEY_INPUT])
            self.assertEqual(response,test_case[KEY_EXPECTED])
            
            
            
    def test_bot(self):
        self.test_params = [
            {
                KEY_TYPE: "ABOUT",
                KEY_INPUT: "!! about",
                KEY_EXPECTED: "Hi, I am BobbyBot. I am a pretty fun guy. If there is something you need from me let me know. To find out what I am capable of typ !! help"
            },
            {
                KEY_TYPE: "HELP",
                KEY_INPUT: "!! help",
                KEY_EXPECTED: "!! about - learn about me<br>!! help - shows this screen<br>!! funtranslate {message} - translate message to {language}<br>!! flip - flip a coin<br>!! bitcoin - I will tell you bitcoins price"
            },
            {
                KEY_TYPE: "FUNTRANSLATE",
                KEY_INPUT: "!! funtranslate Testing this is fun.",
                KEY_EXPECTED: "esting-Tay is-thay is-way un-fay.  "
            }, 
            {
                KEY_TYPE: "FUNTRANSLATE",
                KEY_INPUT: "!! funtranslate Super Duper Fun!",
                KEY_EXPECTED: "uper-Say uper-Day un-Fay! "
            },
            {
                KEY_TYPE: "BITCOIN",
                KEY_INPUT: "!! bitcoin",
                KEY_EXPECTED: "1 bitcoin is currently worth money"
            },
            {
                KEY_TYPE: "FLIP",
                KEY_INPUT: "!! flip",
                KEY_EXPECTED: "TEST"
            },
            {
                KEY_TYPE: "FLIP",
                KEY_INPUT: "!! flip",
                KEY_EXPECTED: "TEST"
            },
            {
                KEY_TYPE: "FLIP",
                KEY_INPUT: "!! flip",
                KEY_EXPECTED: "TEST"
            },
            {
                KEY_TYPE: "FAIL",
                KEY_INPUT: "!! test",
                KEY_EXPECTED: "I don't know how to do that"
            },
            {
                KEY_TYPE: "FAIL",
                KEY_INPUT: "!! !! bitcoin",
                KEY_EXPECTED: "I don't know how to do that"
            },
            {
                KEY_TYPE: "FAIL",
                KEY_INPUT: "!! apple",
                KEY_EXPECTED: "I don't know how to do that"
            },
        ]
            
            
        for test_case in self.test_params:
            response = bot(test_case[KEY_INPUT])
            if test_case[KEY_TYPE] == 'FUNTRANSLATE' and response[:5] == 'Sorry':
                test_case[KEY_EXPECTED] = 'Sorry the limit for translations has been reached'
            elif test_case[KEY_TYPE] == 'BITCOIN' and "1 bitcoin is currently worth " in response:
                test_case[KEY_EXPECTED] = response
            elif test_case[KEY_TYPE] == 'FLIP' and ("HEADS" in response or "TAILS" in response):
                test_case[KEY_EXPECTED] = response
            self.assertEqual(response,test_case[KEY_EXPECTED])
    
if __name__ == '__main__':
    unittest.main()