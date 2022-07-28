from dotenv import load_dotenv
import os
import requests

load_dotenv()
load_dotenv(dotenv_path=os.getcwd())
TMDB_KEY = os.getenv("TMDB_KEY")

GENRE_LEGEND = {'28': 'Action', '12': 'Adventure', '16': 'Animation', '35': 'Comedy', '80': 'Crime', 
                '99': 'Documentary', '18': 'Drama', '10751': 'Family', '14': 'Fantasy', '36': 'History', 
                '27': 'Horror', '10402': 'Music', '9648': 'Mystery', '10749': 'Romance', 
                '878': 'Science Fiction', '10770': 'TV Movie', '53': 'Thriller', '10752': 'War', 
                '37': 'Western'}

# Movie should be recorded with release year to help with search results

class Recommendations():
    """
    Searches each item in the input list to retrieve movie IDs. Then calls the recommendation
    endpoint to get recommendations for each movie. Then returns the top ten recommended movies.
    Occurrence is the number of times it was recommended by the calls.
    Usage:
        reccs = Recommendations(movie_list)
        top_10 = reccs.get_reccs()
        json = reccs.json()
    """
    def __init__(self, movie_list) -> None:
        self.movie_list = movie_list
        
    def get_ids(self):
        """
        Search from TMBD to retrieve movie IDs, and genre ids. 
        Input: [movie_list]
        Output: movie_ids{name:id (int)}, genre_count{name (id): count (int)}
        """
        self.movie_ids = {}
        self.genre_count = {}
        for movie in self.movie_list:
            r = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_KEY}&language=en-US&query={movie}&page=1&include_adult=true")
            json = r.json()
            '''
            be selective of the year if want to select for movie, not story
            be selective of the story, to get similar story elements

            '''
            results = [json['results'][0]] #selective of movie, not story. only getting first result
            # results = json['results'] # more selective of the story, results of different makes of same story
            for result in results:
                movie_id = result['id']
                genre_ids = result['genre_ids']
                # movie = result['original_title'] # uncommont this for selective of the story, not movie
                self.movie_ids[movie] = movie_id
                for id in genre_ids:
                    id = str(id)
                    genre_name = GENRE_LEGEND[id]
                    key = f'{genre_name} ({id})'
                    if self.genre_count.get(key):
                        self.genre_count[key] += 1
                    else:
                        self.genre_count[key] = 1
        
    def get_recc_count(self):
        ids = self.movie_ids.values()
        self.recc_count = {}
        for id in ids:
            json = requests.get(f"https://api.themoviedb.org/3/movie/{id}/recommendations?api_key={TMDB_KEY}&language=en-US&page=1").json()
            for result in json['results']:
                id = result['id']
                title = result['title']
                key = f'{title} ({id})'
                if not self.movie_ids.get(title):
                    if self.recc_count.get(key):
                        self.recc_count[key] += 1
                    else:
                        self.recc_count[key] = 1
                        
    def get_reccs(self):
        """
        Returns:
            list: title (id) (occurence)
        """
        self.get_ids()
        self.get_recc_count()
        self.reccs = []
        highest_count = max(self.recc_count.values())
        list_length = 10
        while len(self.reccs) < list_length:
            for recc in self.recc_count:
                if self.recc_count[recc] == highest_count:
                    self.reccs.append(f'{recc} (Occurrence: {self.recc_count[recc]})')
                    if len(self.reccs) == list_length:
                        break
            highest_count -= 1
        return self.reccs
    
    def json(self):
        """Returns json of recommendations.

        Returns:
            dict: {
                results: [
                        {   
                            "title": str, 
                            "id": int, 
                            "occurrence": int
                        },
                    ]
                }
        """
        res = {}
        res['results'] = []
        for recc in self.reccs:
            add_recc = {}
            recc_split = recc.split(" (")
            title = recc_split[0]
            id = recc_split[1][:-1]
            occurrence = recc_split[2].split(": ")[1][:-1]
            add_recc["title"] = title
            add_recc['id'] = int(id)
            add_recc['occurrence'] = int(occurrence)
            res['results'].append(add_recc)
        return res

