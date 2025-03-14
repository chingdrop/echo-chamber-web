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
        if auth:
            self.session.auth = auth
        if headers:
            self.session.headers.update(headers)

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