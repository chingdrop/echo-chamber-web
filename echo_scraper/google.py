import requests
import logging
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import sleep
from urllib.parse import unquote


class RestAdapter:
    """Rest adapter class uses persistent session and sets default cofiguration.

    Args:
        base_url (str): The base URL for the API
        headers (dict): Default headers (optional)
        auth (Any): Authentication information (optional)
        proxies (dict): Dictionary of proxy addresses for HTTP(s) (optional)
        logger (Logger): Custom logger object (optional)
    """
    def __init__(
            self,
            base_url: str='',
            headers: dict={},
            auth=None,
            proxies: dict={},
            logger=None
    ):
        self.base_url = base_url
        self.logger = logger or logging.getLogger(__name__)

        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)
        if auth:
            self.session.auth = auth
        if proxies:
            self.session.proxies.update(proxies)

    def _send_request(
            self,
            method: str,
            endpoint: str,
            data: dict={},
            params: dict={},
            cookies: dict={},
            verify: bool | str=None,
            timeout: int=None,
            allow_redirects: bool=True
    ) -> dict:
        """Prepare the request to be sent. Send the prepared request and return the response.

        Args:
            method (str): HTTP method ('GET', 'POST', etc.)
            endpoint (str): API endpoint (e.g., '/users', '/posts')
            params (dict): URL parameters (optional)
            data (dict): Data to send in the request body (optional)
            cookies (dict): Data to be used as the cookie in the request (optional)
            verify (bool | str): Boolean whether to enforce SSL authentication, or supply a certificate to use (optional)
            timeout (int): Number of seconds to wait for a response (optional)
            allow_redirects (bool): Allow HTTP redirects to different URLs (optional)

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        self.logger.debug(f'Request [{method}] - {self.base_url} {endpoint}')
        url = self.base_url + endpoint
        req = requests.Request(method,
                               url,
                               headers=self.session.headers,
                               params=params,
                               data=data,
                               cookies=cookies)
        prep_req = self.session.prepare_request(req)
        try:
            response = self.session.send(prep_req,
                                         verify=verify,
                                         timeout=timeout,
                                         allow_redirects=allow_redirects)
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

    def get(
            self,
            endpoint: str,
            params: dict=None,
            cookies: dict=None,
            verify: bool | str=None,
            timeout: int=None,
            allow_redirects: bool=True
    ) -> dict:
        """Make a GET request.

        Args:
            endpoint (str): API endpoint
            params (dict): URL parameters (optional)
            cookies (dict): Data to be used as the cookie in the request (optional)
            verify (bool | str): Boolean whether to enforce SSL authentication, or supply a certificate to use (optional)
            timeout (int): Number of seconds to wait for a response (optional)
            allow_redirects (bool): Allow HTTP redirects to different URLs (optional)

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        return self._send_request('GET',
                                  endpoint,
                                  params=params,
                                  cookies=cookies,
                                  verify=verify,
                                  timeout=timeout,
                                  allow_redirects=allow_redirects)

    def post(
            self,
            endpoint: str,
            data: dict=None,
            params: dict=None,
            cookies: dict=None,
            verify: bool | str=None,
            timeout: int=None,
            allow_redirects: bool=True
    ) -> dict:
        """Make a POST request.

        Args:
            endpoint (str): API endpoint
            data (dict): Data to send in the request body
            params (dict): URL parameters (optional)
            cookies (dict): Data to be used as the cookie in the request (optional)
            verify (bool | str): Boolean whether to enforce SSL authentication, or supply a certificate to use (optional)
            timeout (int): Number of seconds to wait for a response (optional)
            allow_redirects (bool): Allow HTTP redirects to different URLs (optional)

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        return self._send_request('POST',
                                  endpoint,
                                  data=data,
                                  params=params,
                                  cookies=cookies,
                                  verify=verify,
                                  timeout=timeout,
                                  allow_redirects=allow_redirects)

    def put(
            self,
            endpoint: str,
            data: dict=None,
            params: dict=None,
            cookies: dict=None,
            verify: bool | str=None,
            timeout: int=None,
            allow_redirects: bool=True
    ) -> dict:
        """Make a PUT request.

        Args:
            endpoint (str): API endpoint
            data (dict): Data to send in the request body
            params (dict): URL parameters (optional)
            cookies (dict): Data to be used as the cookie in the request (optional)
            verify (bool | str): Boolean whether to enforce SSL authentication, or supply a certificate to use (optional)
            timeout (int): Number of seconds to wait for a response (optional)
            allow_redirects (bool): Allow HTTP redirects to different URLs (optional)

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        return self._send_request('PUT',
                                  endpoint,
                                  data=data,
                                  params=params,
                                  cookies=cookies,
                                  verify=verify,
                                  timeout=timeout,
                                  allow_redirects=allow_redirects)

    def delete(
            self,
            endpoint: str,
            params: dict=None,
            cookies: dict=None,
            verify: bool | str=None,
            timeout: int=None,
            allow_redirects: bool=True
    ) -> dict:
        """Make a DELETE request.

        Args:
            endpoint (str): API endpoint
            params (dict): URL parameters (optional)
            cookies (dict): Data to be used as the cookie in the request (optional)
            verify (bool | str): Boolean whether to enforce SSL authentication, or supply a certificate to use (optional)
            timeout (int): Number of seconds to wait for a response (optional)
            allow_redirects (bool): Allow HTTP redirects to different URLs (optional)

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        return self._send_request('DELETE',
                                  endpoint,
                                  params=params,
                                  cookies=cookies,
                                  verify=verify,
                                  timeout=timeout,
                                  allow_redirects=allow_redirects)
    

class GoogleSearch:
    def __init__(self, proxy=None, logger=None):
        ua = UserAgent()
        headers = {
            'User-Agent': ua.chrome,
            'Accept': "*/*",
        }
        proxies = {"https": proxy, "http": proxy} \
            if proxy and (proxy.startswith("https") or proxy.startswith("http") or proxy.startswith("socks5")) \
            else None
        self.rest = RestAdapter(headers=headers, proxies=proxies, logger=logger)
        self.logger = logger or logging.getLogger(__name__)
        
    def _request(self, term: str, results: int, lang: str, start: int, safe: str, region: str):
        params = {
            'q': term,
            'num': results + 2,
            'hl': lang,
            'start': start,
            'safe': safe,
            'gl': region
        }
        cookies = {
            'CONSENT': 'PENDING+987',
            'SOCS': 'CAESHAgBEhIaAB',
        }
        return self.rest.get('https://www.google.com/search',
                                 params=params,
                                 cookies=cookies,
                                 timeout=5)
    
    def _parse_results(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        result_block = soup.find_all("div", class_="ezO2md")
        for result in result_block:
            link_tag = result.find("a", href=True)
            title_tag = link_tag.find("span", class_="CVA68e") if link_tag else None
            description_tag = result.find("span", class_="FrIlee")

            if link_tag and title_tag and description_tag:
                link = unquote(link_tag["href"].split("&")[0].replace("/url?q=", ""))
                title = title_tag.text if title_tag else ""
                description = description_tag.text if description_tag else ""
                yield {
                    'link': link,
                    'title': title,
                    'description': description
                }

    def search(self, term, results, safe, start, lang, region, unique=False):
        fetched_results = 0
        fetched_links = set()

        while fetched_results < results:
            response_text = self._request(term, results, safe, start, lang, region)
            if not response_text:
                break  # Stop the search if the request fails

            new_results = 0
            for search_result in self._parse_results(response_text):
                if search_result.link in fetched_links and unique:
                    continue  # Skip this result if the link is not unique

                fetched_links.add(search_result.link)
                fetched_results += 1
                new_results += 1
                yield search_result

                if fetched_results >= results:
                    return  # Stop if we have fetched the desired number of results

            if new_results == 0:
                logging.info(f"Only {fetched_results} results found for query requiring {results} results.")
                break  # Break the loop if no new results were found in this iteration

            start += 10
            sleep(120)  # Avoid hitting Google's rate limits
