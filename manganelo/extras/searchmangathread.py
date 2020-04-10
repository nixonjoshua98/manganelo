import threading

from manganelo.api import SearchManga


class SearchMangaThread(SearchManga):
    def __init__(self, query: str):
        super(SearchMangaThread, self).__init__(query)

        self._thread = threading.Thread(target=super(SearchMangaThread, self).start)

    def start(self):
        self._thread.start()

    def wait(self):
        self._thread.join()

    def done(self):
        return not self._thread.is_alive()

    def __enter__(self):
        self.start()

        return self


