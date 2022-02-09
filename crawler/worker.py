from threading import Thread
import datetime
from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time
import pytz
from pytz import timezone
from bs4 import BeautifulSoup
import requests
import urllib.request


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        # Time stamp snippet
        utc = datetime.datetime.now(tz=pytz.utc)
        current = utc.astimezone(timezone('US/Pacific'))
        # Set config variables
        
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        # Output data collection variables
        self.tokenMap = {}
        self.content = open("output/content.txt", "a")
        self.tolkein_content = open("output/tolkein_content.txt", "a")
        # Open max word file to track words in text content per page
        self.maxWordFile = open("output/maxWordFile.txt", "a")
        # Time stamp at the top
        self.maxWordFile.write(f'Crawler Start time: {current}\n')
        self.maxWordFile.flush()
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests from scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        current_max = 0
        current_max_link = ''
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                utc = datetime.datetime.now(tz=pytz.utc)
                current = utc.astimezone(timezone('US/Pacific'))
                self.maxWordFile.write(f'{current_max_link} {current_max}\n')
                self.maxWordFile.write(f'Crawler End time: {current}\n')
                self.maxWordFile.close()
                self.frontier.output.close()
                self.frontier.unique.close()
                break
            
            resp = download(tbd_url, self.config, self.logger)
            if resp.raw_response is not None and scraper.is_valid(tbd_url) and resp.status == 200:
                soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
                text_string = soup.get_text(strip = True)
                max_words = len(text_string.split())
                if max_words < 51:
                    continue
                text_tokens = scraper.tokenize(text_string)
                if current_max < max_words:
                    current_max = max_words
                    current_max_link = tbd_url
                self.maxWordFile.write(f'{tbd_url} {max_words}\n')
                self.maxWordFile.flush()
                tokenMap = scraper.wordFreq(text_tokens)
                orderedTokens = sorted(tokenMap.items(), key=lambda token: token[1], reverse=True)
                for i in orderedTokens:
                    self.content.write(f'{i[0]} {i[1]}\n')
                self.content.flush()
                self.tolkein_content.flush()
                self.logger.info(
                    f"Downloaded {tbd_url}, status <{resp.status}>, "
                    f"using cache {self.config.cache_server}.")
            scraped_urls = scraper.scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
