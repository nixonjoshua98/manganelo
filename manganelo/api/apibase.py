import requests
import threading
import urllib.parse


class APIBase:
	def __init__(self, threaded):
		if threaded:
			# Create and start a new thread to send the request.

			self._thread: threading.Thread = threading.Thread(target=self._start)

			self._thread.start()

		else:
			# Single-threaded - We call the start method on the main thread
			self._start()

	def _join_thread(self):
		""" Handles the extra thread by joining it onto the main thread. """

		# If a thread object exists and it is still active, wait for it to finish.
		if hasattr(self, "_thread") and self._thread.is_alive():
			self._thread.join()

	def _start(self) -> None:
		raise NotImplementedError()

	@staticmethod
	def send_request(url: str) -> requests.Response:
		"""
		Send a request to the URL provided

		:param str url: The URL which we are sending a GET request to.
		:raise: Will raise exceptions from the requests module
		:return: The response object or None
		"""

		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'}

		return requests.get(url, stream=True, timeout=5, headers=headers)

	@staticmethod
	def send_request_image(url: str) -> requests.Response:
		"""
		Send a request to the URL provided

		:param str url: The URL which we are sending a GET request to.
		:raise: Will raise exceptions from the requests module
		:return: The response object or None
		"""
		domain = urllib.parse.urlparse(url).netloc

		header = {
			'Accept': 'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5',
			'Accept-Encoding': 'gzip, deflate, br',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
			'Host': domain, 'Accept-Language': 'en-ca', 'Referer': 'https://manganelo.com/',
			'Connection': 'keep-alive'
		}

		r = requests.get(url, stream=True, timeout=5, headers=header)

		return r
