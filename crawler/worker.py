from threading import Thread

from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time
from bs4 import BeautifulSoup


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.tokenMap = {}
        self.content = open("output/content.txt", "a")
        self.tolkein_content = open("output/tolkein_content.txt", "a")
        self.maxWordFile = open("output/maxWordFile.txt", "a")
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests from scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                for url in self.frontier.downloaded_urls:
                    self.frontier.unique.write(f'{url}\n')
                self.frontier.unique.flush()
                break
            resp = download(tbd_url, self.config, self.logger)
            if resp.raw_response is not None:
                soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
                #text_string = soup.get_text()
                text_string = soup.get_text(strip = True)
                max_words = len(text_string.split())
                text_tokens = scraper.tokenize(text_string)
                tolkein_tokens = scraper.tolkeinizer(text_string)
                #max_words = scraper.maxWords(text_string)
                self.maxWordFile.write(f'{tbd_url} {max_words}\n')
                self.maxWordFile.flush()
                tokenMap = scraper.wordFreq(text_tokens)
                tolkeinMap = scraper.wordFreq(tolkein_tokens)
                orderedTokens = sorted(tokenMap.items(), key=lambda token: token[1], reverse=True)
                orderedTolkeins = sorted(tolkeinMap.items(), key=lambda token: token[1], reverse=True)
                for i in orderedTokens:
                    self.content.write(f'{i[0]} {i[1]}\n')
                for i in orderedTolkeins:
                    self.tolkein_content.write(f'{i[0]} {i[1]}\n')
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