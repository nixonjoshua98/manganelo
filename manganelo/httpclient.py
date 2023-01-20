import collections
import threading
import time
import urllib.parse

import requests

from manganelo.common.constants import ROOT_URL


class _RateLimiter:
    def __init__(self, max_calls, period):
        self.calls = collections.deque()

        self.period = period
        self.max_calls = max_calls
        self.lock = threading.Lock()

    def __enter__(self):
        with self.lock:
            if len(self.calls) >= self.max_calls:
                until = time.time() + self.period - self._timespan
                sleeptime = until - time.time()
                if sleeptime > 0:
                    time.sleep(sleeptime)
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with self.lock:
            self.calls.append(time.time())

            while self._timespan >= self.period:
                self.calls.popleft()

    @property
    def _timespan(self):
        return self.calls[-1] - self.calls[0]


class HTTPClient:
    def __init__(self):
        self.__limiter = _RateLimiter(10, 1)  # 10 reqs/seconds

    def request(self, method, url, **kwargs):
        with self.__limiter:
            r = requests.request(method=method, url=url, **kwargs)
        return r

    def fetch_image(self, url):
        headers = {
            'Accept': 'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'Version/13.1.2 Safari/605.1.15',
            'Host': urllib.parse.urlparse(url).netloc, 'Accept-Language': 'en-ca', 'Referer': ROOT_URL,
            'Connection': 'keep-alive'
        }
        return self.request("GET", url, headers=headers, stream=True)


_default_http_client = HTTPClient()
