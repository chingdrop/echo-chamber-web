import logging
import re
from pathlib import Path
from bs4 import BeautifulSoup
from celery import shared_task

from crawler.api_utils import RestAdapter
from echo_chamber.helpers import delete_files_in_directory, save_text_to_file


logger = logging.getLogger('crawler')


class WebCrawler:
    def __init__(
            self,
            target_url='',
            logger=None
    ):
        self.data_dir = Path.cwd() / 'crawler' / 'data'
        delete_files_in_directory(self.data_dir)

        self.target_url = target_url
        self.logger = logger or logging.getLogger(__name__)
        self.rest = RestAdapter(logger=self.logger)

    def _parse_url(self,):
        pattern = r"^https?:\/\/([a-zA-Z0-9-]+\.)?([a-zA-Z0-9-]+)\.[a-zA-Z]{2,}(?:\:[0-9]+)?(\/[a-zA-Z0-9-\/\?&=.#]*)?$"

    def _create_rest(self,):
        pass

    def get_robot(self,):
        return self.rest.get('/robots.txt')

    def snap_url(self, url):
        self.logger.debug(f'Getting contents of {url}')
        path = ""
        res = self.rest.get(url)
        pattern = r'^https?:\/\/([a-zA-Z0-9-]+)\.[a-z]{2,}(\/[a-zA-Z0-9-\/]+)?$'
        search = re.search(pattern, url)
        if search:
            if search.group(2):
                path = search.group(2).replace('/', '_')
            file_name = f'{search.group(1)}{path}.html'
            self.logger.debug(f'Saving HTML to {file_name}')
            save_text_to_file(self.data_dir / file_name, content=res, encoding='utf-8')
        return res

    def get_next_links(self, url):
        res = self.rest.get(url)
        soup = BeautifulSoup(res, 'html.parser')
        links = soup.find_all('a')
        urls = []
        for link in links:
            href = link['href']
            https_pattern = r'^https?:\/\/([a-zA-Z0-9-]+)\.[a-z]{2,}(\/[a-zA-Z0-9-\/]+)?$'
            match = re.match(https_pattern, href)
            if match:
                urls.append(match.group())
            elif '/' in href and href != '/':
                urls.append(url + href)
        self.logger.debug(f'Found {len(urls)} URLs')
        return urls


@shared_task
def crawl_website(url):
    wc = WebCrawler(logger=logger)
    wc.snap_url(url)
    next_urls = wc.get_next_links(url)
    for next_url in next_urls:
        wc.snap_url(next_url)