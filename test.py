import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup


url = "https://wics.ics.uci.edu/events/2021-04-22"
parsed = urlparse(url)
#p = parsed.path.lower().split("/")
print(parsed.path.lower())
if re.findall(r"\d{4}-\d{2}-\d{2}$", parsed.path.lower()):
    print("Hello World")
#if re.findall(r"\d{4}-\d{2}-\d{2}$/", p[2]):
    #print("Hello World")
