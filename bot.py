"""Parse message and return the proper bot response"""
import random
import requests


#based on command respond with bot
def bot(message):
    """Parse message and return the proper bot response"""
    spltmsg = message.split()
    cmd = spltmsg[1]
    if cmd == 'about': # description of bot
        return ('Hi, I am BobbyBot. I am a pretty fun guy. If there is something you need from' +
        ' me let me know. To find out what I am capable of type !! help')
    if cmd == 'help': # command list
        ret = "!! about - learn about me<br>"
        ret += "!! help - shows this screen<br>"
        ret += "!! funtranslate {message} - translate message to {language}<br>"
        ret += "!! flip - flip a coin<br>"
        ret += "!! bitcoin - I will tell you bitcoins price"
        return ret
    if cmd == 'flip': # flip a coin
        coin = random.getrandbits(1)
        if coin == 1:
            return 'The coin landed HEADS up'
        return 'The coin landed TAILS up'

    if cmd == 'funtranslate': # translate to piglatin
        url = "https://api.funtranslations.com/translate/pig-latin.json?text="
        for i in range(2,len(spltmsg)):
            url+=spltmsg[i] + '+'
        req=requests.get(url)
        data = req.json()
        try:
            ret = data["contents"]["translated"][:-2]
        except:
            ret = "Sorry the limit for translations has been reached"
        return ret

    if cmd == 'bitcoin': # message the price of bitcoin
        url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        req=requests.get(url)
        data = req.json()
        return ("1 bitcoin is currently worth "
        + data["bpi"]["USD"]["symbol"] + ""
        + data["bpi"]["USD"]["rate"])

    # command doesn't exist
    return "I don't know how to do that"
