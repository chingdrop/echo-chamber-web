from pathlib import Path

from echochamber.logger import setup_logger
from crawler.api import WebCrawler


logger = setup_logger('crawler-tasks', level='debug')

def crawl_website():
    wc = WebCrawler(logger=logger)
    data_dir = Path.cwd() / 'crawler' / 'data'
    wc.snap_url('https://healthishot.co', data_dir)
    urls = wc.get_next_links('https://healthishot.co')
    for url in urls:
        wc.snap_url(url, data_dir)