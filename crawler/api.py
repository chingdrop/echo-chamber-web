import re
import logging
import requests
from bs4 import BeautifulSoup
from pathlib import Path

from echochamber.helpers import save_text_to_file, delete_files_in_directory


class RestAdapter:
    def __init__(
            self,
            base_url: str='',
            headers: dict=None,
            auth=None,
            logger=logging.getLogger()
    ):
        """Initialize the RequestHandler instance.

        Args:
            base_url (str): The base URL for the API
            headers (dict): Default headers (optional)
            auth: Authentication information (optional)
        """
        self.base_url = base_url
        self.headers = headers if headers else {}
        self.auth = auth
        self.logger = logger

        self.session = requests.Session()
        if self.auth:
            self.session.auth = self.auth
        if self.headers:
            self.session.headers.update(self.headers)

    def _send_request(
            self,
            method: str,
            endpoint: str,
            params: dict=None,
            data: dict=None
    ) -> dict:
        """Prepare the request to be sent. Send the prepared request and return the response.
        
        Args:
            method (str): HTTP method ('GET', 'POST', etc.)
            endpoint (str): API endpoint (e.g., '/users', '/posts')
            params (dict): URL parameters (optional)
            data (dict): Data to send in the request body. (optional)
        
        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        self.logger.debug(f'Request [{method}] - {self.base_url} {endpoint}')
        url = self.base_url + endpoint
        req = requests.Request(method, url, headers=self.session.headers, params=params, data=data)
        prep_req = self.session.prepare_request(req)
        try:
            response = self.session.send(prep_req)
            response.raise_for_status()
            self.logger.debug(f'Status [{response.status_code}] - {response.reason}')
            if response:
                content_type = response.headers.get('Content-Type', '').lower()
                if 'application/json' in content_type:
                    return response.json()
                elif 'text/html' in content_type:
                    return response.text
                else:
                    return response.content
        except requests.exceptions.HTTPError as errh:
            self.logger.error(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            self.logger.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            self.logger.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            self.logger.error(f"An Unexpected Error: {err}")

    def get(self, endpoint: str, params: dict=None) -> dict:
        """Make a GET request.
        
        Args:
            endpoint (str): API endpoint
            params (dict): URL parameters (optional)

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        return self._send_request('GET', endpoint, params=params)

    def post(self, endpoint: str, data: dict=None) -> dict:
        """Make a POST request.

        Args:
            endpoint (str): API endpoint
            data (dict): Data to send in the request body.

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        return self._send_request('POST', endpoint, data=data)

    def put(self, endpoint: str, data: dict=None) -> dict:
        """Make a PUT request.

        Args:
            endpoint (str): API endpoint
            data (dict): Data to send in the request body.

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        return self._send_request('PUT', endpoint, data=data)

    def delete(self, endpoint: str, params: dict=None) -> dict:
        """Make a DELETE request.

        Args:
            endpoint (str): API endpoint
            params (dict): URL parameters (optional)

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        return self._send_request('DELETE', endpoint, params=params)


class WebCrawler:
    def __init__(self, logger=logging.getLogger()):
        self.data_dir = Path.cwd() / 'crawler' / 'data'
        delete_files_in_directory(self.data_dir)
        self.logger = logger
        self.rest = RestAdapter(logger=logger)

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
