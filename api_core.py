import requests
from dialog import lang
from datetime import date, timedelta


# API requester
class APIcon:
    def __init__(self):
        self.__url = "https://api.themoviedb.org/3/"
        self.__url_prefix = ""
        self.__headers = None
        self.__params = {}
        self.list_current_page = 1

    def set_key(self, key: str):
        self.__headers = {"accept": "application/json", "Authorization": f"Bearer {key}"}

    def test(self):
        res = requests.get(self.__url + "authentication", headers=self.__headers, params=self.__params)
        return res.json()

    def get_movie_search(self, value: str):
        self.__params = {"include_adult": "True", "language": lang.language.keyword, "query": value,
                         "page": self.list_current_page}
        try:
            res = requests.get(self.__url + "search/movie", headers=self.__headers, params=self.__params)
            return res.json()
        except Exception as e:
            print(e)
            return None

    def get_movie_details(self, mov_id: int):
        self.__params = {"language": lang.language.keyword, "append_to_response": "videos"}
        try:
            res = requests.get(self.__url + f"/movie/{mov_id}", headers=self.__headers, params=self.__params).json()
        except Exception as e:
            print(e)
            return None
        if res['videos']['results']:
            trailer_link = f"https://youtu.be/{res['videos']['results'][0]['key']}={res['videos']['results'][0]['id']}"
        else:
            trailer_link = 'Empty'
        poster_link = f"https://image.tmdb.org/t/p/w500{res['poster_path']}"
        imdb_link = f"https://www.imdb.com/title/{res['imdb_id']}"
        return {"genres": ", ".join(x['name'].replace('-', '\\-').replace('!', '\\!') for x in res['genres']),
                "imdb": imdb_link,
                "poster": poster_link,
                "release_date": res['release_date'].replace('-', '\\-'),
                "title": res['title'].replace('-', '\\-').replace('.', '\\.')
                .replace('!', '\\!').replace(')', '\\)').replace('(', '\\('),
                "trailer": trailer_link,
                "overview": res['overview'].replace('-', '\\-').replace('.', '\\.')
                .replace('!', '\\!').replace(')', '\\)').replace('(', '\\(')}

    def get_tv_search(self, value: str):
        self.__params = {"include_adult": "True", "language": lang.language.keyword, "query": value,
                         "page": self.list_current_page}
        try:
            res = requests.get(self.__url + "search/tv", headers=self.__headers, params=self.__params)
            return res.json()
        except Exception as e:
            print(e)
            return None

    def get_tv_details(self, mov_id: int):
        self.__params = {"language": lang.language.keyword, "append_to_response": "videos"}
        try:
            res = requests.get(self.__url + f"/tv/{mov_id}", headers=self.__headers, params=self.__params).json()
        except Exception as e:
            print(e)
            return None
        if res['videos']['results']:
            trailer_link = f"https://youtu.be/{res['videos']['results'][0]['key']}={res['videos']['results'][0]['id']}"
        else:
            trailer_link = 'Empty'
        poster_link = f"https://image.tmdb.org/t/p/w500{res['poster_path']}"
        return {"genres": ", ".join(x['name'].replace('-', '\\-') for x in res['genres']),
                "poster": poster_link,
                "release_date": res['first_air_date'].replace('-', '\\-'),
                "title": res['name'].replace('-', '\\-').replace('.', '\\.')
                .replace('!', '\\!').replace(')', '\\)').replace('(', '\\('),
                "trailer": trailer_link,
                "seasons_count": res['number_of_seasons'],
                "overview": res['overview'].replace('-', '\\-').replace('.', '\\.')
                .replace('!', '\\!').replace(')', '\\)').replace('(', '\\('),
                "status": lang.language.message_tv_status_ended if res['status'] == "Ended" else
                lang.language.message_tv_status_ongoing}

    def get_tv_trending_day(self):
        self.__params = {"language": lang.language.keyword, "page": self.list_current_page}
        try:
            res = requests.get(self.__url + '/trending/tv/day', headers=self.__headers, params=self.__params)
            return res.json()
        except Exception as e:
            print(e)
            return None

    def get_tv_trending_week(self):
        self.__params = {"language": lang.language.keyword, "page": self.list_current_page}
        try:
            res = requests.get(self.__url + '/trending/tv/week', headers=self.__headers, params=self.__params)
            return res.json()
        except Exception as e:
            print(e)
            return None

    def get_movie_trending_day(self):
        self.__params = {"language": lang.language.keyword, "page": self.list_current_page}
        try:
            res = requests.get(self.__url + '/trending/movie/day', headers=self.__headers, params=self.__params)
            return res.json()
        except Exception as e:
            print(e)
            return None

    def get_movie_trending_week(self):
        self.__params = {"language": lang.language.keyword, "page": self.list_current_page}
        try:
            res = requests.get(self.__url + '/trending/movie/week', headers=self.__headers, params=self.__params)
            return res.json()
        except Exception as e:
            print(e)
            return None

    def get_movie_upcoming(self):
        self.__params = {"language": lang.language.keyword,
                         "page": self.list_current_page,
                         "primary_release_date.gte": date.today(),
                         "primary_release_date.lte": date.today() + timedelta(weeks=11)}
        try:
            res = requests.get(self.__url + '/discover/movie', headers=self.__headers, params=self.__params)
            return res.json()
        except Exception as e:
            print(e)
            return None


req = APIcon()
