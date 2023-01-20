import manganelo

home = manganelo.get_home_page()

results = manganelo.get_search_results("attack on titan")

for r in results:
    print(r)
