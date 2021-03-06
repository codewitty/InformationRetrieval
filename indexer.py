import json
import re
import os, sys
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
token_count = {}
tf_dict ={}

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
        writeToDisk(inverted_index, count)
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

# Convert all queries from the input into a list 
def convertQueryToList(somestring):
    global queries_list
    queries_list = list()
    for queries in somestring.split(" "):
            queries_list.append(queries.strip())

def search(query, someList, output_dir):
    global count
    postings_list = []
    p = SnowballStemmer("english")
    # Remove duplicates
    someList = list(set(someList))
    for element in someList:
        element_l = element.lower()
        element_l = p.stem(element_l)
        flag = False

        for filename in os.listdir(output_dir):
            f = os.path.join(output_dir, filename)
            with open(f) as index_file:
                data_c = (index_file.read())
            temp_index = json.loads(data_c)
            if element_l in temp_index.keys():
                posting = temp_index[element_l]
                #print(f'Keyword {element} was stemmed into {element_l} found in these pages:{posting}')
                posting.pop(0)
                for posting in list(set(posting)):
                    postings_list.append(posting)
                print(type(postings_list))
                print(len(postings_list))
                break
        '''
        if not flag:
            print(f'Search Query {element} not found')

    if len(postings_list) > 1:
        t = len(postings_list) # number of files contains the token
        df = t/count
        idf = math.log(count/(df+1))
        for token in someList:
            token = token.lower() 
            print(token)
            tfidf = {}
            #doc_id = 0
            for url in postings_list:
                #tc = token_count[url][token]#the number of token found in that url
                #tf = tc / total_word[url] #num of token found / #total word count
                #tfidf[url] = (doc_id[url], tf * idf)
            #tf_dict[token] = dict(sorted(tfidf.items(), key=lambda item: item[1][1],reverse=True))
        result = 0
        all_q = {}
        q_count = 0

        for q in someList:
            if q.lower() != "and":
                q_count +=1

        for q in someList:
            for k,v in someList[q].items():
                 if k not in all_q:
                     all_q[k] = [v[0],v[1], 1]
                 else:
                     all_q[k][2] +=1
                     if all_q[k][1]> v[1]:
                         all_q[k][1] = v[1]


        for k,v in dict(sorted(all_q.items(),key=lambda item: item[1][1],reverse=True)).items():
            if v[2] == q_count:
                result +=1
                print(f"RANKED RESULTS")
                print(f"url: {k}, docID: {v[0]}")

        if(result == 0):
            print("No match found")
            return
        '''

    repeats = "~~~~~~~~~" * 20
    if len(someList) > 1:
        intersection = set.intersection(*postings_list)
        #print(postings_list[0].intersection(*postings_list))
        print(f'{repeats}')
        if len(intersection) > 0:
            print(f"RANKED RESULTS")
            print(f'Search query {query} found in {len(intersection)} pages: {intersection}')
        else:
            print(f'Search Query: {query} NOT FOUND')
        print(f'{repeats}')
    elif len(someList) == 1 and len(postings_list) > 1:
        print(f'{repeats}')
        print(f"RANKED RESULTS")
        print(f'Search query {query} found in {len(postings_list)} pages:')
        print(*postings_list, sep = "\n")
        print(f'{repeats}')
    else:
        print(f'NO RESULTS FOUND')
        

def writeToDisk(index, count = 100, filenames = 'output_indexes/output'):
    filename = filenames + str(count) + ".json"
    with open (filename, "w") as outfile:
        json_object = json.dumps(index, indent=4, sort_keys=True)
        outfile.write(json_object)

def mergeIndexes(output_dir):
    global inverted_index
    for filename in os.listdir(output_dir):
        f = os.path.join(output_dir, filename)
        with open(f) as index_file:
            data_c = (index_file.read())
            temp_index = json.loads(data_c)

        for posting in temp_index.keys():
            if posting in inverted_index.keys():
                temp_list  = temp_index[posting]
                temp_list.pop(0)
                for page in temp_list:
                    if page not in inverted_index[posting]:
                        inverted_index[posting].append(page)
                        inverted_index[posting][0] += 1
            else:
                inverted_index[posting] = temp_index[posting]

def splitIndex(index, chunks=50):
    "Return list of split indexes"
    return_list = [dict() for idx in range(chunks)]
    idx = 0
    for k,v in index.items():
        return_list[idx][k] = v
        if idx < chunks-1:  # indexes start at 0
            idx += 1
        else:
            idx = 0
    return return_list

if __name__ == '__main__':
    directory = sys.argv[1]
    query_directory = sys.argv[2]
    output_directory = sys.argv[3]
    tf_directory = sys.argv[4]
    total_word_file = tf_directory + '/total_word.json'
    doc_id_file = tf_directory + '/doc_id.json'
    token_count_file = tf_directory + '/token_count.json'
    """
    start = time.time()
    output_check = Path(output_directory)
    query_check = Path(query_directory)
    tf_check = Path(tf_directory)
    if not output_check.exists():
        os.mkdir(output_directory)
    if not query_check.exists():
        os.mkdir(query_directory)
    if not tf_check.exists():
        os.mkdir(tf_directory)
    output_index = 'inverted_index_final.json'
    buildIndex(directory)

    # Merge all Indexes
    mergeIndexes(output_directory)
    
    # Write final tf index to disk:
    with open (total_word_file, "w") as outfile:
        json_object = json.dumps(total_word, indent=4, sort_keys=True)
        outfile.write(json_object)

    with open (doc_id_file, "w") as outfile:
        json_object = json.dumps(doc_id, indent=4, sort_keys=True)
        outfile.write(json_object)

    with open (token_count_file, "w") as outfile:
        json_object = json.dumps(token_count, indent=4, sort_keys=True)
        outfile.write(json_object)


    split_indexes = splitIndex(inverted_index, 100)

    dict_count = 1

    query_subdirectory = query_directory + '/query_dict'

    for index in split_indexes:
        writeToDisk(index, dict_count, query_subdirectory)
        dict_count+=1

    # Time measurement
    end = time.time()
    mins = (end - start)/60
    print(f'Start Time: {start}')
    print(f'End Time: {end}')
    print(f'Time taken: {mins}')
    """

    #Querying the DB
    flag = True
    while(flag):
        queries_input = input('Enter your query here: ')
        convertQueryToList(queries_input)
        # Load the tf indexes

        with open(total_word_file) as index_file:
            data_c = (index_file.read())
        total_word = json.loads(data_c)

        with open(doc_id_file) as index_file:
            data_c = (index_file.read())
        doc_id = json.loads(data_c)

        with open(token_count_file) as index_file:
            data_c = (index_file.read())
        token_count = json.loads(data_c)

        print(f'Queries are: {queries_list}')
        start2 = time.time()
        for filename in os.listdir(query_directory):
            f = os.path.join(query_directory, filename)
            with open(f) as index_file:
                data_c = (index_file.read())
            temp_index = json.loads(data_c)
            count += len(temp_index)
        print(f'~~~~~~~~~Global Count = {count}~~~~~~~~~~~~')
        search(queries_input, queries_list, query_directory)
        # Time measurement
        end2 = time.time()
        mins = ((end2 - start2)/60) * 1000
        print(f'Time taken for query: {mins} ms')
        response = input("Would you like to search again. Type any key for yes or n/N for no\n")
        if response.lower() == "n":
            flag = False
            print(f'Thank you for using this search engine. Goodbye!')
