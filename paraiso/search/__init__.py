import requests

IMDB_API = "https://v3.sg.media-imdb.com/suggestion/x/{term}.json?includeVideos=0"


def get_imdb_movies(title_term):
    response = requests.get(IMDB_API.format(term=title_term))
    if not response.ok:
        return []
    content = response.json()
    movies = content.get("d", [])
    return [m for m in movies if m.get("id").startswith("tt")]
