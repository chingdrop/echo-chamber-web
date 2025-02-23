from pathlib import Path

from crawler.api import WebCrawler


def crawl_website():
    wc = WebCrawler()
    data_dir = Path.cwd() / 'crawler' / 'data'
    wc.snap_url('https://healthishot.co', data_dir)
    urls = wc.get_next_links('https://healthishot.co')
    for url in urls:
        wc.snap_url(url, data_dir)