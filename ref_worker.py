from threading import Thread

from utils.download import download
from utils import get_logger
from scraper import scraper
import time
from urllib.parse import urlparse


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            # add frontier lock
            # self.frontier.fLock.acquire()
            tbd_url = self.frontier.get_tbd_url()

            # # examin domain lock, set accordingly
            # domain = urlparse(tbd_url).netloc

            # if ".ics.uci.edu" in domain:
            #     self.frontier.icsLock.acquire()
            # elif ".cs.uci.edu" in domain:
            #     self.frontier.csLock.acquire()
            # elif "informatics.uci.edu" in domain:
            #     self.frontier.infoLock.acquire()
            # elif ".stat.uci.edu" in domain:
            #     self.frontier.statLock.acquire()
            # elif "today.uci.edu" in domain:
            #     self.frontier.todayLock.acquire()

            # # release frontier lock 
            # self.frontier.fLock.release()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            
            # self.frontier.scrap.acquire()
            scraped_urls = scraper(tbd_url, resp)
            # self.frontier.scrap.release()
            

            # self.frontier.fLock.acquire()
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
                # release F
            # self.frontier.fLock.release()


            # MIGHT NOT BE NEEDED
            # lock F
            self.frontier.mark_url_complete(tbd_url)
            # release F
            
            
            time.sleep(self.config.time_delay)
            # release domain lock
            
            # if ".ics.uci.edu" in domain:
            #     self.frontier.icsLock.release()
            # elif ".cs.uci.edu" in domain:
            #     self.frontier.csLock.release()
            # elif "informatics.uci.edu" in domain:
            #     self.frontier.infoLock.release()
            # elif ".stat.uci.edu" in domain:
            #     self.frontier.statLock.release()
            # elif "today.uci.edu" in domain:
            #     self.frontier.todayLock.release()
