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
            #self.logger.info(
                #f"Downloaded {tbd_url}, status <{resp.status}>, "
                #f"using cache {self.config.cache_server}.")
            scraped_urls = scraper.scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
                soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
                text_string = soup.get_text()
                text_tokens = scraper.tokenize(text_string)
                tokenMap = scraper.wordFreq(text_tokens)
            #scraper.printFreq(tokenMap)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)