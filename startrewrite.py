
import manganelo.rewrite as manganelo

results = manganelo.search(title="Naruto")

first = results[0]

page = manganelo.manga_page(url=first.url)

chapters = first.chapter_list()
# manganelo.chapters(url=first.url)

chap_one = chapters[0]

print(chapters)

# path = chap_one.download(path=f"D:\\Repos\\manganelo\\{chap_one.title}.pdf")
# manganelo.download(url=chap_one.url, path=...)

# print(path)  # D:\Repos\manganelo\Vol.1 Chapter 0  Naruto Pilot Manga.pdf
