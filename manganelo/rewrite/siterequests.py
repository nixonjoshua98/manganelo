import requests
import urllib.parse

_DEFAULT_HEADERS = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"
}

_ROOT  = "http://manganelo.com/"


def search(title):
	return get(f"{_ROOT}search/story/{title}")


def get(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'}

	return requests.get(url, stream=True, timeout=10, headers=headers)


def dl_image(url):
	domain = urllib.parse.urlparse(url).netloc

	header = {
		'Accept': 'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
		'Host': domain, 'Accept-Language': 'en-ca', 'Referer': _ROOT,
		'Connection': 'keep-alive'
	}

	return requests.get(url, stream=True, timeout=10, headers=header)