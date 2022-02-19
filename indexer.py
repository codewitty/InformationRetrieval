import json
import os
import tokenizer
from bs4 import BeautifulSoup
import zipfile
import time
from nltk.stem.snowball import SnowballStemmer


count = 0
inverted_index = {}
total_word = {}
doc_id = {}
def checkEnglish(str):
    try:
        str.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        print("All Good")
        return True

def getContent(filename):
    global count
    global inverted_index
    f = open(filename, "r")
    data = json.load(f)
    url = data['url']
    print(url)
    soup = BeautifulSoup(data['content'], 'html.parser')
    text_string = soup.get_text(strip = True)
    text_tokens = tokenizer.tokenize(text_string)
    total_word[url] = len(text_tokens)
    for token in text_tokens:
        if token in inverted_index.keys() and url not in inverted_index[token]:
            inverted_index[token][0] += 1
            inverted_index[token].append(url)
        else:
            lst = [1, url]
            inverted_index[token] = lst

    #self.maxWordFile.flush()
    doc_id[url] = count
    count += 1
    print(count)

def getContent_nonUni(filename):
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


def buildIndex(directory):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file

        if os.path.isfile(f):
            try:
                getContent(f)
            except UnicodeDecodeError:
                #print("We are trying to decode now")
                #getContent_nonUni(f)
                continue

        elif os.path.isdir(f):
            buildIndex(f) 

#convert all queries from the input into a list, store AND bool queries in a set
#then append into the lst
def query_lst(somestring):
    global queries_list
    queries_list = list()
    for queries in somestring.split(" "):
            queries_list.append(queries.strip())

def search(someList):
    postings_list = []
    p = SnowballStemmer("english")
    for element in someList:
        element_l = element.lower()
        element_l = p.stem(element_l)
        if element_l in inverted_index.keys():
            posting = inverted_index[element_l]
            print(f'Keyword {element} was found in these pages:{posting}')
            posting.pop(0)
            postings_list.append(set(posting))
        else:
            print(f'Search Query {element} not found')
    if len(postings_list) > 1:
        intersection = set.intersection(*postings_list)
        #print(postings_list[0].intersection(*postings_list))
        print(f'Intersection List: {intersection}')

def get_idf(token):
    t = inverted_index[token][0] # number of files contains the token
    df = t/count
    idf = math.log(count/(df+1))
    return idf
    
def get_tfidf(token):
    tfidf = []
    #doc_id = 0
    if token.lower() in inverted_index.keys():
        for url in inverted_index[token]:
            token_count = ininverted_index[token][0]#the number of token found in that url
            tf = token_count / total_word[url] #num of token found / #total word count
            tfidf.append(set(url, doc_id[url], tf * get_idf(token)))
    
    return tfidf


if __name__ == '__main__':
    queries_input = input('Enter your query here: ')
    query_lst(queries_input)
    print(f'Queries are: {queries_list}')
"""
    directory = '/Users/joshuagomes/InformationRetrieval/DEV_Final'
    archive = "output.zip"
    start = time.time()
    buildIndex(directory)
    end = time.time()
    mins = (end - start)/60
    print(f'Start Time: {start}')
    print(f'End Time: {end}')
    print(f'Time taken: {mins}')
    print(f'Number of tokens: {len(inverted_index)}')
    print(f'Number of documents: {count}')
    with open ("output_nltkStem.json", "w") as outfile:
        json_object = json.dumps(inverted_index, indent=4, sort_keys=True)
        print(f'Size of jSON Data Structure: {str((json_object.__sizeof__()))}')
        outfile.write(json_object)
"""
    with open("output_nltkStem.json") as f:
        data_c = (f.read())

    inverted_index = json.loads(data_c)
    print(len(inverted_index))
    search(queries_list)

"""
    with zipfile.ZipFile(archive, "w") as comp:
        comp.write("output.json")
        
    with zipfile.ZipFile(archive, "r") as zf:
        crc_test = zf.testzip()
        if crc_test is not None:
            print(f"Bad CRC or file headers: {crc_test}")
        with zf.open("output.json") as f:
            data_c = (f.read().decode())
    print(type(data_c))
    data = json.loads(data_c)
    print(f'Size of Decompressed jSON Data Structure: {str((data.__sizeof__()))}')
    term = 'would'
    if term in data.keys():
        print(f'\n\n\nFound {data[term]}\n\n\n')
    else:
        print(f'Not found!!!')
    print(f'Size of Loaded Data Structure: {str((data.__sizeof__()))}')
"""
