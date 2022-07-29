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
print(recc.get_reccs())
print(recc.json())
print(recc.filter_streaming_availability(provider="Netflix"))