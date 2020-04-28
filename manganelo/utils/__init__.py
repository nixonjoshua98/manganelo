import requests


def send_request(url: str, *, timeout: int = 5) -> requests.Response:
    """
    Send a request to the URL provided

    :param str url: The URL which we are sending a GET request to.
    :param timeout: Optional parameter which decides how long we wait before throwing an exception
    :raise: Will raise exceptions from the requests module
    :return: The response object
    """

    default_headers = requests.utils.default_headers()

    r = requests.get(url, stream=True, timeout=timeout, headers=default_headers)

    r.raise_for_status()

    return r
