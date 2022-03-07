import json
import re
import os
import os.path
from pathlib import Path
import tokenizer
from bs4 import BeautifulSoup
import zipfile
import time
import math
from nltk.stem.snowball import SnowballStemmer
from lxml.html.clean import Cleaner
from lxml import etree


count = 0
inverted_index = {}
invalid_pages = []
json_error_pages = []
error_list = []
total_word = {}
doc_id = {}
token_count ={}

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
    """
    if content == "":
        print('Empty Doc')
        return
    if len(content) < 5:
        print('Empty Doc')
        return
    """
    soup = BeautifulSoup(content, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    text_string = soup.get_text(strip = True)
    text_tokens = tokenizer.tokenize(text_string)
    total_word[url] = len(text_tokens)
    token_count[url] ={}
    for token in text_tokens:
        if token in inverted_index.keys():
            if token in token_count[url].keys():
                token_count[url][token] += 1
            else:
                token_count[url][token]  = 1
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
    if count % 10000 == 0:
        writeToDisk(inverted_index)
        inverted_index = {}

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

# Convert all queries from the input into a list, store AND bool queries in a set
# then append into the list
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
    t = len(inverted_index[token]) # number of files contains the token
    df = t/count
    idf = math.log(count/(df+1))
    return idf
    
def get_tfidf(q_list):
    tf_dict ={}
    for token in q_list:
        tfidf = {}
        #doc_id = 0
        if token in inverted_index.keys():
            for url in inverted_index[token]:
                tc = token_count[url][token]#the number of token found in that url
                tf = tc / total_word[url] #num of token found / #total word count
                tfidf[url] = (doc_id[url], tf * get_idf(token))
        tf_dict[token] = dict(sorted(tfidf.items(), key=lambda item: item[1][1],reverse=True))
    return tf_dict

def print_result(td):
    print("Ranked by tf-idf")
    for q in td:
        print(f"Query: {q}")
        for k,v in td[q].items():
            print(f"url: {k}, docID: {v[0]}")

def writeToDisk(index):
    global count
    filename = "output_indexes/output" + str(count) + ".json"
    with open (filename, "w") as outfile:
        json_object = json.dumps(index, indent=4, sort_keys=True)
        outfile.write(json_object)

def mergeIndexes(output_dir):
    global inverted_index
    print(f'Length of original index before starting = {len(inverted_index)}')
    for filename in os.listdir(output_dir):
        f = os.path.join(output_dir, filename)
        with open(f) as index_file:
            data_c = (index_file.read())
            temp_index = json.loads(data_c)
            print(f'Length of index from {filename} = {len(temp_index)}')

        for posting in temp_index.keys():
            if posting in inverted_index.keys():
                temp_list  = temp_index[posting]
                for page in temp_list:
                    if page not in inverted_index[posting]:
                        inverted_index[posting].append(page)
                        inverted_index[posting][0] += 1
            else:
                inverted_index[posting] = temp_index[posting]
    #os.rmdir(output_dir)

if __name__ == '__main__':
    #directory = '/Users/joshuagomes/InformationRetrieval/DDev'
    directory = '/Users/joshuagomes/InformationRetrieval/Dev'
    #directory = '/Users/joshuagomes/InformationRetrieval/DEV_Final'
    archive = "output.zip"
    start = time.time()
    output_directory = "/Users/joshuagomes/InformationRetrieval/output_indexes"
    output_check = Path(output_directory)
    if not output_check.exists():
        os.mkdir(output_directory)
    output_index = 'inverted_index_final.json'
    buildIndex(directory)
    # Time measurement
    end = time.time()
    mins = (end - start)/60
    print(f'Start Time: {start}')
    print(f'End Time: {end}')
    print(f'Time taken: {mins}')

    # Merge all Indexes
    mergeIndexes(output_directory)
    
    # Write final merged index to disk:
    with open (output_index, "w") as outfile:
        json_object = json.dumps(inverted_index, indent=4, sort_keys=True)
        outfile.write(json_object)

    # Sanity checks
    print(f'Number of tokens: {len(inverted_index)}')
    print(f'Number of documents: {count}')
    print(f'Invalid Pages: {invalid_pages}')
    print(f'JSON error Pages: {json_error_pages}')
    print(f'Etree Error Pages: {error_list}')

    with open("inverted_index_final.json") as f:
        data_c = (f.read())
    index2 = json.loads(data_c)
    print(f'Number of tokens Merged Index: {len(index2)}')

"""
    #Querying the DB
    queries_input = input('Enter your query here: ')
    query_lst(queries_input)
    print(f'Queries are: {queries_list}')
    inverted_index = json.loads(data_c)
    print(json.dumps(inverted_index, indent=4))
    buildIndex(directory)
    search(queries_list)
    print_result(get_tfidf(queries_list))
"""
