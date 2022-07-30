from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

load_dotenv()
load_dotenv(dotenv_path=os.getcwd())
TMDB_KEY = os.getenv("TMDB_KEY")

GENRE_LEGEND = {'28': 'Action', '12': 'Adventure', '16': 'Animation', '35': 'Comedy', '80': 'Crime', 
                '99': 'Documentary', '18': 'Drama', '10751': 'Family', '14': 'Fantasy', '36': 'History', 
                '27': 'Horror', '10402': 'Music', '9648': 'Mystery', '10749': 'Romance', 
                '878': 'Science Fiction', '10770': 'TV Movie', '53': 'Thriller', '10752': 'War', 
                '37': 'Western'}

# TODO compare do most common keyword analysis using imdb and beautiful soup
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
        #TODO revise to have a more efficient way to get reccs by streaming provider.
        # while len(self.reccs) < list_length: #
        while highest_count > 0:
            for recc in self.recc_count:
                if self.recc_count[recc] == highest_count:
                    self.reccs.append(f'{recc} (Occurrence: {self.recc_count[recc]})')
                    # if len(self.reccs) == list_length:
                    #     break
            highest_count -= 1
        return self.reccs[:10] # Return the top 10 reccs
    
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

    def filter_streaming_availability(self, provider='Disney Plus', country='US'):
        """Calls the provider availability endpoint and selects for US by defualt.

        Args:
            provider (_type_): _description_
        """
        # ['Reservoir Dogs (500) (Occurrence: 11)', 'Transformers (1858) (Occurrence: 9)', 'The Departed (1422) (Occurrence: 8)', 'Pulp Fiction (680) (Occurrence: 8)', '300 (1271) (Occurrence: 7)', 'Se7en (807) (Occurrence: 7)', 'TRON: Legacy (20526) (Occurrence: 6)', 'The A-Team (34544) (Occurrence: 6)', 'Hancock (8960) (Occurrence: 6)', 'Taken (8681) (Occurrence: 6)']
        recc_by_avail = []
        for recc in self.reccs:
            if len(recc_by_avail) == 10:
                break
            movie_id = recc.split(" (")[1][:-1]
            r = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={TMDB_KEY}")
            results = r.json()["results"]
            if results.get(country):
                results = results[country]
                if results.get("flatrate"):
                    results = results['flatrate']
                    for result in results:
                        if result['provider_name'] == provider:
                            recc_by_avail.append(recc)
        return recc_by_avail

    def get_imdb_ids(self):
        movie_ids = []
        for recc in self.reccs:
            id = recc.split(" (")[1][:-1]
            movie_ids.append(id)
        self.imdb_ids = []
        for movie_id in movie_ids:
        # for movie_id in movie_ids[:10]:
            r = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/external_ids?api_key={TMDB_KEY}")
            json = r.json()
            self.imdb_ids.append(json['imdb_id'])

        # For when checking the keywords of movie_list
        # movie_ids = []
        # for recc in self.movie_ids:
        #     id = self.movie_ids[recc]
        #     movie_ids.append(id)
        # self.imdb_ids = []
        # for movie_id in movie_ids:
        # # for movie_id in movie_ids[:10]:
        #     r = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/external_ids?api_key={TMDB_KEY}")
        #     json = r.json()
        #     self.imdb_ids.append(json['imdb_id'])

    def get_imdb_keywords(self):
        self.get_imdb_ids()
        res = []
        exceptions = []
        for imdb_id in self.imdb_ids:
            r = requests.get(f"https://www.imdb.com/title/{imdb_id}/keywords?ref_=tt_stry_kw")
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.find(class_="dataTable evenWidthTable2Col")
            try:
                rows = table.find_all('tr')
                for row in rows:
                    for col in row.find_all('td'):
                        item = ''
                        for i, ele in enumerate(col):
                            if i == 1: # Keyword
                                for j, line in enumerate(ele):
                                    if j == 1:
                                        for keyword in line:
                                            item += keyword
                            if i == 3:
                                for j, line in enumerate(ele):
                                    if j == 1:
                                        for k, ele2 in enumerate(line):
                                            if k == 1:
                                                for aba in ele2:
                                                    amount = aba.split(" ")
                                                    amount = [amount[1], amount[3]]
                                                    # if amount[1] == '1':
                                                    if amount[1] == '1' or amount[1] == '2':
                                                        item = ""
                                                    elif amount[0] == amount[1]:
                                                        item += f' {amount[0]}/{amount[1]}'
                                                    else:
                                                        item = ""
                        if len(item) > 0:
                            res.append(item) 
            except:
                exceptions.append(imdb_id)

        return res, exceptions