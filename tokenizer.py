import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from porterStemming import PorterStemmer

tokenMap = {}

def checkEnglish(str):
    try:
        str.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True
    
def tokenize(somestring):
    p = PorterStemmer()
    tokenList = []
    newline = somestring.rstrip()
    string = list(re.findall('([^-_\s\'\t\.]+)', newline))                
    for word in string:
        if word == "":
            continue
        if not checkEnglish(word):
            continue
        if not word.isalpha():
            continue
        word = word.lower()
        #word = re.sub(r"[^a-zA-Z0-9]","",word)
        word = p.stem(word, 0, len(word) - 1)
        tokenList.append(word)
    return tokenList

def maxWords(somestring):
    maxWordCount = 0
    newline = somestring.rstrip()
    string = list(re.findall('([^-_\s\'\t\.]+)', newline))                
    for word in string:
        if not checkEnglish(word):
            continue
        word = word.lower()
        word = re.sub(r"[^a-zA-Z0-9]","",word)
        if word == "":
            continue
        maxWordCount+=1
    return maxWordCount

def wordFreq(tokenList):
    tokenMap = {}
    for word in tokenList:
        if word in tokenMap.keys():
            tokenMap[word] += 1
        else:
            tokenMap[word] = 1
    return tokenMap

def printFreq(tokenMap):
    orderedTokens = sorted(tokenMap.items(), key=lambda token: token[1], reverse=True)

    for i in orderedTokens:
        print(f'{i[0]}\t{i[1]}')
