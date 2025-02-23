from celery import shared_task

from echochamber.logger import setup_logger
from crawler.api import WebCrawler


logger = setup_logger('crawler-tasks', level='debug')

@shared_task
def crawl_website(url):
    wc = WebCrawler(logger=logger)
    wc.snap_url(url)
    next_urls = wc.get_next_links(url)
    for next_url in next_urls:
        wc.snap_url(next_url)