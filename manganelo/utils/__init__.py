import requests


def send_request(url: str) -> requests.Response:
    """
    Send a request to the URL provided

    :param str url: The URL which we are sending a GET request to.
    :raise: Will raise exceptions from the requests module
    :return: The response object or None
    """

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'}

    r = requests.get(url, stream=True, timeout=5, headers=headers)

    return r
