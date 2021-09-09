import manganelo

results = manganelo.get_search_results("Naruto")

for r in results:
    print(r.title, r.views)

    chapters = r.chapter_list()

    icon_path = r.download_icon("./icon.png")

    for c in chapters:
        print(f"#{c.chapter} | {c.title}")

        chapter_path = c.download(f"./Chapter {c.chapter}.pdf")
