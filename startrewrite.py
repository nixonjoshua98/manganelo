import manganelo.rewrite as manganelo

results = manganelo.search(title="Naruto")

for r in results:
    print(r.title, r.views)

    chapters = r.chapter_list()

    for c in chapters:
        print(f"#{c.chapter} | {c.title}")

        chapter_path = c.download(path=f"./Chapter {c.chapter}.pdf")
