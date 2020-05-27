import unittest

from manganelo import DownloadChapter


class Testing(unittest.TestCase):
    def test_download(self):
        obj = DownloadChapter("https://manganelo.com/chapter/aq920543/chapter_148", "../../junk/MA C 148.pdf")

        results = obj.results()

        self.assertEqual(results.percent_saved, 1.0)

    def test_download_403(self):
        obj = DownloadChapter(
            "https://mangakakalots.com/chapter/dead_dead_demons_dededededestruction/chapter_0",
            "../../junk/DungeonDestruction C 0.pdf"
        )

        results = obj.results()

        self.assertEqual(results.saved_ok, True)


if __name__ == "__main__":
    unittest.main()
