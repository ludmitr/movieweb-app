import requests
import logging

class MovieAPIHandler():
    IMDB_PATH = "https://www.imdb.com/title/"

    def __init__(self):
        self._api_key = "f994fda"
        self._url = "https://www.omdbapi.com/"
        self._logger = logging.getLogger(__name__)

    def get_movie_by_title(self, title: str) -> dict:
        """Search for movie by title. Returns dict with data of found movie
        and None if didn't find movie"""
        params = {
            'apikey': self._api_key,
            't': title
        }
        try:
            # get the search result, transform the data to match app needs and return the data
            response = requests.get(self._url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            if response.json()["Response"] == 'True':
                processed_movie_data = self._transform_movie_data(response.json())
                return processed_movie_data

        except requests.exceptions.RequestException as e:
            # self._logger.error(f"An error occurred: {str(e)}")
            pass
        # case of exceptions or movie didn't found
        return None

    def _transform_movie_data(self, api_data: dict) -> dict:
        """Transform api data to match the data used in app"""
        transformed_data = {
            'id': api_data['imdbID'],
            'name': api_data['Title'],
            'director': api_data['Director'],
            'year': api_data['Year'],
            'rating': api_data['imdbRating'],
            'imdb_link': MovieAPIHandler.IMDB_PATH + api_data['imdbID'],
            'image_link': api_data['Poster']
        }
        return transformed_data


