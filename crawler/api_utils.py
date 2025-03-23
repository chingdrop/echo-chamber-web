import requests
import logging


class RestAdapter:
    """Rest adapter class makes interacting with APIs easy.

    Args:
        base_url (str): The base URL for the API
        headers (dict): Default headers (optional)
        auth (Any): Authentication information (optional)
        logger (Logger): Custom logger object (optional)
    """
    def __init__(
            self,
            base_url: str='',
            headers: dict={},
            auth=None,
            logger=None
    ):
        self.base_url = base_url
        self.logger = logger or logging.getLogger(__name__)

        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)
        if auth:
            self.session.auth = auth

    def _send_request(
            self,
            method: str,
            endpoint: str,
            data: dict={},
            params: dict={},
            cookies: dict={},
            verify: bool | str=True,
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
            allow_redirects (bool): Allow HTTP redirects to different URLs

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
            verify: bool | str=True,
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
            allow_redirects (bool): Allow HTTP redirects to different URLs

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
            verify: bool | str=True,
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
            allow_redirects (bool): Allow HTTP redirects to different URLs

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
            cookies: dict=None,
            verify: bool | str=True,
            timeout: int=None,
            allow_redirects: bool=True
    ) -> dict:
        """Make a PUT request.

        Args:
            endpoint (str): API endpoint
            data (dict): Data to send in the request body.
            cookies (dict): Data to be used as the cookie in the request (optional)
            verify (bool | str): Boolean whether to enforce SSL authentication, or supply a certificate to use (optional)
            timeout (int): Number of seconds to wait for a response (optional)
            allow_redirects (bool): Allow HTTP redirects to different URLs

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        return self._send_request('PUT',
                                  endpoint,
                                  data=data,
                                  cookies=cookies,
                                  verify=verify,
                                  timeout=timeout,
                                  allow_redirects=allow_redirects)

    def delete(
            self,
            endpoint: str,
            params: dict=None,
            cookies: dict=None,
            verify: bool | str=True,
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
            allow_redirects (bool): Allow HTTP redirects to different URLs

        Returns:
            dict: JSON serialized response body or None if an error occurs.
        """
        return self._send_request(
            'DELETE', endpoint, params=params, cookies=cookies, verify=verify, timeout=timeout
        )
