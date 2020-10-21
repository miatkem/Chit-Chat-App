import requests
def parsePicturesAndLinks(msg):
    ret = ""
    words=msg.split()
    for word in words:
        if word[-4:] == '.jpg' or word[-4:] == '.png' or word[-4:] == '.gif':
            
            valid=False
            try:
                response = requests.get(word)
                valid=True
            except:
                valid=False
            if valid:
                ret+="<img src='"+word+"' class='msgImg'/>"
            else:
                ret+=word
        elif word[:6] == 'https:' or word[:5] == 'http:' or word[:4] == 'www.' or word[:-4] == '.com' or word[:-4] == '.net' or word[:-4] == '.org' or word[:-4] == '.edu' or word[:-4] == '.org':
            valid=False
            try:
                response = requests.get(word)
                valid=True
            except:
                valid=False
            if valid:
                ret+="<a href='"+word+"' target='_blank'>"+word+"</a>"
            else:
                ret+=word
        else:
            ret+=word
        
        ret += " "
    return ret