import re
from urllib.parse import urlparse, urldefrag
from bs4 import BeautifulSoup



def scraper(url, resp):
    links = extract_next_links(url, resp)
    # for x in links:
    #     if is_valid(x):
    #         print(x)
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
    
    
    #print(f'THIS IS A {resp.error}')
    print()
    s = set()
    if resp.status/100 == 2:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        for link in soup.find_all('a'):
            if link.get('href') != None:
                unfragmented = link.get('href').split('#')[0]
            
                s.add(unfragmented)
                              
            #l.append(str(link.get('href')))
    return list(s)
    


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    
    try:
        parsed = urlparse(url)
        if ('.ics.uci.edu/' in url) or ('.cs.uci.edu/' in url) or ('.informatics.uci.edu/' in url) or ('.stat.uci.edu/' in url) or ('today.uci.edu/department/information_computer_sciences/' in url):
            
            invalid_set = {'wics.ics.uci.edu/events', 'wics.ics.uci.edu/week', 'wics.ics.uci.edu/wics', 'evoke.ics.uci.edu/about/'}
            
            for invalid in invalid_set:
                if invalid in url:
                    return False
            
            if parsed.scheme not in set(["http", "https"]) or ('files/' in url) or ('pdf/' in url) or ('.pdf' in url):
                return False
            return not re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz|flac|txt|py)$", parsed.path.lower())
        else:
            return False

    except TypeError:
        print ("TypeError for ", parsed)
        raise
