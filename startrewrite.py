
import manganelo.rewrite as manganelo

results = manganelo.search(title="Naruto")

first = results[0]

chapters = first.chapter_list()
# or chapters = manganelo.chapters(url=first.url)

chap_one = chapters[0]

path = chap_one.download(path=f"D:\\Repos\\manganelo\\{chap_one.title}.pdf")
# or path = manganelo.download(url=chap_one.url, path=...)

print(path)  # D:\Repos\manganelo\Vol.1 Chapter 0  Naruto Pilot Manga.pdf
