import json
import os
import porterStemming
import tokenizer
from bs4 import BeautifulSoup

count = 0

def checkEnglish(str):
    try:
        str.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        print("All Good")
        return True

def print_words(filename):
    global count
    f = open(filename, "r")
    o = open("output_tokens.txt", "a")
    data = json.load(f)
    url = data['url']
    print(url)
    soup = BeautifulSoup(data['content'], 'html.parser')
    text_string = soup.get_text(strip = True)
    text_tokens = tokenizer.tokenize(text_string)
    #self.maxWordFile.flush()
    o.write(f'{url}: {text_tokens}\n')
    count += 1
    print(count)
#test

def print_words_nonUni(filename):
    global count
    f = tokenize.open(filename)
    """
    if not isinstance(text, bytes):
    text = text.encode('utf-8')
    f = text + (pad * chr(pad)).encode("utf-8")
    """
    #data1 = f.read()
    #data1.encode('ascii', 'ignore')
    data1 = json.loads(f.read())
    print(data1['url'])
    count += 1
    print(count)


def enter(directory):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file

        if os.path.isfile(f):
            try:
                print_words(f)
            except UnicodeDecodeError:
                #print("We are trying to decode now")
                #print_words_nonUni(f)
                continue

        elif os.path.isdir(f):
            enter(f)

if __name__ == '__main__':
    directory = '/Users/joshuagomes/InformationRetrieval/DEV'
    enter(directory)
    
