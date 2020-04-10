import bs4

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
