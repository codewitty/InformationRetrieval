import json
import re
import os
import tokenizer
from bs4 import BeautifulSoup
import zipfile
import time
from nltk.stem.snowball import SnowballStemmer
from lxml.html.clean import Cleaner
from lxml import etree


count = 0
inverted_index = {}
invalid_pages = []
json_error_pages = []
error_list = []

def checkEnglish(str):
    try:
        str.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        print("All Good")
        return True

def sanitize(dirty_html):
    cleaner = Cleaner(page_structure=True,
                  meta=True,
                  embedded=True,
                  links=True,
                  style=True,
                  processing_instructions=True,
                  inline_style=True,
                  scripts=True,
                  javascript=True,
                  comments=True,
                  frames=True,
                  forms=True,
                  annoying_tags=True,
                  remove_unknown_tags=True,
                  safe_attrs_only=True,
                  safe_attrs=frozenset(['src','color', 'href', 'title', 'class', 'name', 'id']),
                  remove_tags=('span', 'font', 'div')
                  )

    return cleaner.clean_html(dirty_html)

def getContent(filename):
    global json_error_pages
    global error_list
    global count
    global inverted_index
    f = open(filename, "r")
    try:
        data = json.load(f)
    except:
        json_error_pages.append(filename)
        return
    url = data['url']
    content = data['content']
    re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\U00010000-\U0010FFFF]+', '', content)
    content = bytes(bytearray(content, encoding='utf-8'))
    """
    if content == "":
        print('Empty Doc')
        return
    if len(content) < 5:
        print('Empty Doc')
        return
    """
    #print(f'\n\n\n\n\n\n\n\n\n{filename}~~~~~~~~~~~~~~~~~~~~~~~~ORIGINAL DATA~~~~~~~~~~~\n{content}')
    try:
        sanitized_data = sanitize(content)
    except (ValueError, etree.ParserError):
        error_list.append(filename)
        return

    #print(f'\n\n\n\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SANITIZED\n{sanitized_data}')
    soup = BeautifulSoup(sanitized_data, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    text_string = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text_string.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text_string = '\n'.join(chunk for chunk in chunks if chunk)
    #print(f'\n\n\n\n\n\n\n\n\n~~~~~~~~~~Text~~~~~~~~~~~~~~~~~~~~~~~~\n{text_string}')
    text_tokens = tokenizer.tokenize(text_string)
    for token in text_tokens:
        if token in inverted_index.keys() and url not in inverted_index[token]:
            inverted_index[token][0] += 1
            inverted_index[token].append(url)
        else:
            lst = [1, url]
            inverted_index[token] = lst

    #self.maxWordFile.flush()
    count += 1
    print(count)

def getContent_nonUni(filename):
    global count
    #print(url)
    count += 1
    """
    f = tokenize.open(filename)
    if not isinstance(text, bytes):
    text = text.encode('utf-8')
    f = text + (pad * chr(pad)).encode("utf-8")
    #data1 = f.read()
    #data1.encode('ascii', 'ignore')
    data1 = json.loads(f.read())
    print(data1['url'])
    count += 1
    print(count)
    """


def buildIndex(directory):
    global invalid_pages
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file

        if os.path.isfile(f):
            try:
                getContent(f)
            except UnicodeDecodeError:
                #print("We are trying to decode now")
                #getContent_nonUni(f)
                invalid_pages.append(f)
                #continue

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
        #element_l = p.stem(element_l)
        if element_l in inverted_index.keys():
            posting = inverted_index[element_l]
            print(f'Keyword {element} was stemmed into {element_l} found in these pages:{posting}')
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
    tf = []
    #doc_id = 0
    tf = 0
    for url in inverted_index[token]:
        
        #the number of token found in that url
        #total word count of the file
        
        tf.append(set(url, tf * get_idf(token)))#num of token found / #total word count
        
    return tf


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
    print(f'Invalid Pages: {invalid_pages}')
    print(f'JSON error Pages: {json_error_pages}')
    print(f'Etree Error Pages: {error_list}')
    with open ("output_noStem.json", "w") as outfile:
        json_object = json.dumps(inverted_index, indent=4, sort_keys=True)
        print(f'Size of jSON Data Structure: {str((json_object.__sizeof__()))}')
        outfile.write(json_object)
    """
    with open("output_noStem.json") as f:
        data_c = (f.read())

    inverted_index = json.loads(data_c)
    print(json.dumps(inverted_index, indent=4))
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
