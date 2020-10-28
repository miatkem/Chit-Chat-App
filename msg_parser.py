"""Functions that parse metadata out of messages"""
import requests


def parse_pictures_and_links(msg):
    """Parse the picture and links in messages"""
    ret = ""
    words=msg.split()
    for word in words:
        if word[-4:] == '.jpg' or word[-4:] == '.png' or word[-4:] == '.gif':

            valid=False
            try:
                requests.get(word)
                valid=True
            except requests.exceptions.RequestException:
                valid=False
            if valid:
                ret+="<img src='"+word+"' class='msgImg'/>"
            else:
                ret+=word
        elif (word[:6] == 'https:' or word[:5] == 'http:' or word[:4] == 'www.'):

            valid=False
            try:
                requests.get(word)
                valid=True
            except requests.exceptions.RequestException:
                valid=False
            if valid:
                ret+="<a href='"+word+"' target='_blank'>"+word+"</a>"
            else:
                ret+=word
        else:
            ret+=word

        ret += " "
    return ret
