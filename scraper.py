import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup


tokenMap = {}

stop_words=["a","about","above","after","again","against","all","am","an","and","any","are","arent","as","at","be","because","been","before","being","below","between","both","but","by","cant","cannot","could","couldnt","did","didnt","do","does","doesnt","doing","dont","down","during","each","few","for","from","further","had","hadnt","has","hasnt","have","havent","having","he","hed","hell","hes","her","here","heres","hers","herself","him","himself","his","how","hows","i","id","ill","im","ive","if","in","into","is","isnt","it","its","its","itself","lets","me","more","most","mustnt","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shant","she","shed","shell","shes","should","shouldnt","so","some","such","than","that","thats","the","their","theirs","them","themselves","then","there","theres","these","they","theyd","theyll","theyre","theyve","this","those","through","to","too","under","until","up","very","was","wasnt","we","wed","well","were","weve","were","werent","what","whats","when","whens","where","wheres","which","while","who","whos","whom","why","whys","with","wont","would","wouldnt","you","youd","youll","youre","youve","your","yours","yourself","yourselves"]
repeat_url = []

# Encodes one character at a time, hence O(n) complexity
def checkEnglish(str):
    try:
        str.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True

# O(n) average time for re.findall where n is number of words, 
# Inside the for loop: O(n) for checkEnglish + O(n) for lower + O(n) for re.sub
def tokenize(somestring):
    tokenList = []
    newline = somestring.rstrip()
    string = list(re.findall('([^-_\s\'\t\.]+)', newline))                
    for word in string:
        if not checkEnglish(word):
            continue
        word = word.lower()
        word = re.sub(r"[^a-zA-Z0-9]","",word)
        if word == "" or word in stop_words:
            continue
        tokenList.append(word)
    return tokenList

# Processes one word at a time, O(n) complexity
def wordFreq(tokenList):
    tokenMap = {}
    for word in tokenList:
        if word in tokenMap.keys():
            tokenMap[word] += 1
        else:
            tokenMap[word] = 1
    return tokenMap

# Average time complexity is O(n log n) for sorting + O(n) to print n tokens
def printFreq(tokenMap):
    orderedTokens = sorted(tokenMap.items(), key=lambda token: token[1], reverse=True)

    for i in orderedTokens:
        print(f'{i[0]}\t{i[1]}')


def scraper(url, resp):
    links = extract_next_links(url, resp)
    if links == None:
        return list()
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    # 2022-01-26 01:41:03,044 - Worker-0 - INFO - Downloaded http://www.informatics.uci.edu/files/pdf/InformaticsBrochure-March2018, status <200>, using cache ('styx.ics.uci.edu', 9005).
    
    #/^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$/

    s = set()
    word_freq = {}
    if resp.status/100 == 2:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        #for div in soup.find_all('div'):
            #if div.get("id" == "data-date"):
                #continue
        for link in soup.find_all('a'):
            #print(f'LINK: {link.get("href")}')
            if link.get('href') != None:
                #print(f'LINK: {link.get("href")}')
                unfragmented = link.get('href')
                unparsed = urlparse(unfragmented)
                parsed_url = unparsed._replace(query="",fragment="").geturl()  
                #print(f'PARSED: {unparsed}')
                s.add(parsed_url)
                #s.add(unfragmented)
        return list(s)
    


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    if ('.ics.uci.edu/' in url) or ('.cs.uci.edu/' in url) or ('.informatics.uci.edu/' in url) or ('.stat.uci.edu/' in url) or ('today.uci.edu/department/information_computer_sciences/' in url):
        
        try:
            parsed = urlparse(url)
            if parsed.scheme not in set(["http", "https"]) or ('files/' in url):
                return False
            if re.match("/^\d{4}-\d{2}-\d{2}$/", parsed.path.lower()):
                print("INSIDE REGEX!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return False
            return not re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz|txt)$", parsed.path.lower())

        except TypeError:
            print ("TypeError for ", parsed)
            raise
    else:
        return False
    
    

    