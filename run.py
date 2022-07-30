from recommender.recc import Recommendations

# Sample movie_list
movie_list = [
    "Ratatouille",
    "The Conjuring",
    "Spider-Man: Into the Spider-Verse",
    "Dune",
    "Shutter Island",
    "Interstellar",
    "Annabelle",
    "Doctor Strange in the Multiverse of Madness",
    "Doctor Strange",
    "Pirates of the Caribbean",
    "Harry Potter",
    "The Wolf of Wall Street"
]

recc = Recommendations(movie_list)
# print(recc.get_reccs())
recc.get_reccs()
# print(recc.json())
# print(recc.filter_streaming_availability(provider="Netflix"))
keywords, exceptions = recc.get_imdb_keywords()
count = {}
for ele in keywords:
    keyword = ''
    name = ele.split(" ")
    for thing in name:
        if "/" not in thing:
            keyword += f'{thing} '
    keyword = keyword[:-1]
    if count.get(keyword):
        count[keyword] += 1
    else:
        count[keyword] = 1
print(count)
print(max(count.values()))
print(len(exceptions), exceptions)

res = []
highest = max(count.values())

while highest > 0:
    for keyword in count:
        if count[keyword] == highest:
            res.append(f'{keyword}: {count[keyword]}')
    highest -= 1

print(res)

print('top10', res[:10])