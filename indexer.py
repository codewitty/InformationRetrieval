import json
import os
import tokenizer
from bs4 import BeautifulSoup
import zipfile

count = 0
inverted_index = {}

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
    global inverted_index
    f = open(filename, "r")
    data = json.load(f)
    url = data['url']
    print(url)
    soup = BeautifulSoup(data['content'], 'html.parser')
    text_string = soup.get_text(strip = True)
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

#convert all queries from the input into a list, store AND bool queries in a set
#then append into the lst
def query_lst(somestring):
    global queries_list
    queries_list = list()
    for queries in somestring.split(","):
        if "AND" in queries:
            queries_list.append(set(queries.strip().split(" AND ")))
        elif "and" in queries:
            queries_list.append(set(queries.strip().split(" and ")))
        else:
            queries_list.append(queries.strip())
            

if __name__ == '__main__':
    queries_input = input('Enter the queries (seperate by ","): ')
    query_lst(queries_input)
    directory = '/Users/joshuagomes/InformationRetrieval/DEV_Final'
    archive = "output.zip"
    enter(directory)
    print(f'Number of tokens: {len(inverted_index)}')
    print(f'Number of documents: {count}')
    with open ("output.json", "w") as outfile:
        json_object = json.dumps(inverted_index, indent=4, sort_keys=True)
        print(f'Size of jSON Data Structure: {str((json_object.__sizeof__()))}')
        outfile.write(json_object)

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
