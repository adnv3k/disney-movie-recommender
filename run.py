from recommender.recc import Recommendations

# Sample movie_list
# Gets list of movies from movie_list.txt
movie_list = []
with open("movie_list.txt") as f:
    movies = f.readlines()
for movie in movies:
    movie_list.append(movie.strip("\n"))

recc = Recommendations(movie_list)
print(recc.get_reccs())
print(recc.json())
print(recc.filter_streaming_availability(provider="Netflix"))