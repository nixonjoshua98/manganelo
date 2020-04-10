import bs4
import requests

from typing import Union

from bs4 import BeautifulSoup

from manganelo.errors import TagNotFound


def find_or_raise(soup: BeautifulSoup, *, class_: str) -> Union[bs4.element.Tag, bs4.element.PageElement]:
    """
    Attempts to find a class inside the soup, if the tag cannot be found then raise an exception.

    :param BeautifulSoup soup:  The soup we will try to find the class <class_> in.
    :param str class_:          The class name we are searching for.
    :return:                    We return the element which is a bs4 Tag, but PyCharm marks it as a bs4 PageElement so
                                we use a Union and mark it as both types.
    """
    element = soup.find(class_=class_)

    if element is None:
        raise TagNotFound(f"Tag not found")

    return element


def send_request(url: str, *, timeout: int = 5) -> requests.Response:
    """
    Send a request to the URL provided

    :param str url: The URL which we are sending a GET request to.
    :param timeout: Optional parameter which decides how long we wait before throwing an exception
    :return: The response object
    """
    default_headers = requests.utils.default_headers()

    r = requests.get(url, stream=True, timeout=timeout, headers=default_headers)

    r.raise_for_status()

    return r
