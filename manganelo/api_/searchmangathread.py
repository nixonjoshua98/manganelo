import threading

from manganelo.api import SearchManga


class SearchMangaThread(SearchManga):
    def __init__(self, title: str):
        super().__init__(title)

        self._thread = threading.Thread(target=super().start)

    def start(self):
        self._thread.start()

    def wait(self):
        while self._thread.is_alive():
            pass

    def done(self):
        return not self._thread.is_alive()

    def __enter__(self):
        self.start()
        return self


