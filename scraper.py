import re
from urllib.parse import urlparse
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
    
    
    print(f'THIS IS A {resp.error}')
    l = list()
    if resp.status/100 == 2:
        print("2")
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        print("3")
        #urls = []
        for link in soup.find_all('a'):
            #if is_valid(link):
            l.append(str(link.get('href')))
    return l
    


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    if ('.ics.uci.edu/' in url) or ('.cs.uci.edu/' in url) or ('.informatics.uci.edu/' in url) or ('.stat.uci.edu/' in url) or ('today.uci.edu/department/information_computer_sciences/' in url):
        
        try:
            parsed = urlparse(url)
            if parsed.scheme not in set(["http", "https"]) or ('files/' in url):
                return False
            return not re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

        except TypeError:
            print ("TypeError for ", parsed)
            raise
    else:
        return False