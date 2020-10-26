import random
import requests

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
        try: 
            ret = data["contents"]["translated"]
        except:
            ret = "Sorry the limit for translations has been reached"
            
        return ret 
        
    elif cmd == 'bitcoin': # message the price of bitcoin
        url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        r=requests.get(url)
        data = r.json()
        return "1 bitcoin is currently worth " + data["bpi"]["USD"]["symbol"] + "" + data["bpi"]["USD"]["rate"]
        
    else: # command doesn't exist
        return "I don't know how to do that"
