from mal.types import TITLE_FIELDS
from os import environ
import requests

DEFAULT_TITLE_FIELDS: TITLE_FIELDS = ['id', 'title', 'num_episodes', 'average_episode_duration', 'related_anime',
                                      'start_date']


class MALClient:
    def __init__(self, client_id: str = environ.get('MAL_CLIENT_ID')):
        self.client_id = client_id
        self.base_url = 'https://api.myanimelist.net'

    def _endpoint(self, endpoint: str):
        if endpoint[:4] == 'http':
            return endpoint
        if endpoint[-1] == '/':
            endpoint = endpoint[:-1]
        if endpoint[0] != '/':
            endpoint = '/' + endpoint

        return self.base_url + endpoint

    def _client_request(self, method: str, endpoint: str, **kwargs):
        headers = kwargs.get('headers', {})
        headers.update({'X-MAL-CLIENT-ID': self.client_id})
        return requests.request(method, self._endpoint(endpoint), headers=headers, **kwargs)

    def search(self, string: str, limit: int = 100):
        endpoint = '/v2/anime'
        return self._client_request('get', endpoint, params={'q': string, 'limit': limit})

    def get_anime_details(self, id: int, fields: TITLE_FIELDS = None):
        fields = fields or DEFAULT_TITLE_FIELDS
        endpoint = f'/v2/anime/{id}'
        return self._client_request('get', endpoint, params={'fields': ','.join(fields)}).json()

