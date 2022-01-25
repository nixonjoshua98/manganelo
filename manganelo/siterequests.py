import requests
import urllib.parse

from manganelo.common.constants import ROOT_URL


def get_image(url):
    header = {
        'Accept': 'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/13.1.2 Safari/605.1.15',
        'Host': urllib.parse.urlparse(url).netloc, 'Accept-Language': 'en-ca', 'Referer': ROOT_URL,
        'Connection': 'keep-alive'
    }

    return requests.get(url, stream=True, timeout=10, headers=header)
