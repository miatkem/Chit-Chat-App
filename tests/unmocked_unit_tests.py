import unittest

import sys
sys.path.append('../')

from msgParser import parsePicturesAndLinks

import unittest.mock as mock
from os.path import join, dirname

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
    
if __name__ == '__main__':
    unittest.main()