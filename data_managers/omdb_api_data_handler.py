import requests

API_KEY = "f994fda"

class MovieAPIHandler():
    def __init__(self):
        self._api_key = "f994fda"
        self._url = "https://www.omdbapi.com/"
    def get_movie_by_title(self, title: str) -> dict:
        """Search for movie by title. Returns dict with data of found movie"""
        params = {
            'apikey': 'f994fda',
            't': title
        }
        try:
            response = requests.get(self._url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            return response.json()  # Parse the response as JSON
        except requests.exceptions.RequestException as e:
            return None



