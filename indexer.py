import json
import os
import tokenizer
from bs4 import BeautifulSoup
import zlib

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
    directory = '/Users/joshuagomes/InformationRetrieval/DDev'
    enter(directory)
    print(f'Number of tokens: {len(inverted_index)}')
    #print(f'Size of Data Structure: {str((inverted_index.__sizeof__()))}')
    with open ("output.json", "w") as outfile:
        json_object = json.dumps(inverted_index, indent=4, sort_keys=True)
        print(f'Size of jSON Data Structure: {str((json_object.__sizeof__()))}')
        outfile.write(json_object)

    with open ("output_compressed.json", "wb") as comp:
        fin = open("output.json", "rb")
        data_in = fin.read()
        compressed_data = zlib.compress(data_in, zlib.Z_BEST_COMPRESSION)
        print(f'Size of Compressed jSON Data Structure: {str((compressed_data.__sizeof__()))}')
        fin.close()
        comp.write(compressed_data)
        
        
    f = open("output.json", "r")
    data = json.load(f)
    term = 'would'
    print(type(data))
    if term in data.keys():
        print(f'\n\n\nFound {data[term]}\n\n\n')
    else:
        print(f'Not found!!!')
    print(f'Size of Loaded Data Structure: {str((data.__sizeof__()))}')
