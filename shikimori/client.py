import json
from os import environ
from os.path import exists
import requests

from mal.types import MAL_TITLE_ID

REFRESH_TOKEN = 'refresh_token'
ACCESS_TOKEN = 'access_token'


class ShikimoriClient:
    def __init__(self, tokens_path: str = environ.get('SHIKIMORI_TOKENS_PATH')):
        if not exists(tokens_path):
            open(tokens_path, 'w').close()

        self.tokens_path = tokens_path
        tokens = self._load_tokens()
        self.access_token, self.refresh_token = tokens[ACCESS_TOKEN], tokens[REFRESH_TOKEN]
        self.base_url = 'https://shikimori.one'

    def _load_tokens(self):
        if not hasattr(self, 'tokens_path'):
            raise Exception('load_tokens is invoked before init passing tokens_path')
        with open(self.tokens_path, 'r') as f:
            tokens = json.load(f)
        return tokens

    def _update_tokens(self):
        with open(self.tokens_path, 'w') as f:
            f.write(json.dumps({
                ACCESS_TOKEN: self.access_token,
                REFRESH_TOKEN: self.refresh_token
            }, indent=3))

    def _endpoint(self, endpoint: str):
        if endpoint[:4] == 'http':
            return endpoint
        if endpoint[-1] == '/':
            endpoint = endpoint[:-1]
        if endpoint[0] != '/':
            endpoint = '/' + endpoint

        return self.base_url + endpoint

    def _request(self, method: str, endpoint: str, **kwargs):
        headers = kwargs.get('headers', {})
        headers.update({'Authorization': 'Bearer %s' % self.access_token, 'User-Agent': 'timeEater'})
        response = requests.request(method, self._endpoint(endpoint), headers=headers, **kwargs)
        if response.status_code != 401:  # Token is ok.
            return response

        self.refresh_tokens()
        headers.update({'Authorization': 'Bearer %s' % self.access_token})
        return requests.request(method, self._endpoint(endpoint), headers=headers, **kwargs)

    def animes(self, search: str):
        endpoint = '/api/animes'
        return self._request('get', endpoint, params={'search': search})

    def anime(self, id: MAL_TITLE_ID):
        endpoint = '/api/animes/%s' % id
        return self._request('get', endpoint)

    def franchise(self, id: MAL_TITLE_ID):
        endpoint = '/api/animes/%s/franchise' % id
        return self._request('get', endpoint)

    def refresh_tokens(self):
        files = {
            'grant_type': (None, 'refresh_token'),
            'client_id': (None, 'CkIrS8TiMrHpTu3IBpEPMUzCXFVpLibrAH26jue0hHo'),
            'client_secret': (None, 'ZMwCr0M6gG00hK3SqTnspn_LtIu6CshiolLM_4W7jnM'),
            'refresh_token': (None, self.refresh_token),
        }
        headers = {
            "User-Agent": 'timeEater'
        }
        response = requests.post(self._endpoint('/oauth/token'),headers=headers, files=files)
        if response.status_code != 200:
            raise Exception('Something is going wrong with refreshing token %s' % response.text)

        response_tokens = response.json()
        self.refresh_token = response_tokens['refresh_token']
        self.access_token = response_tokens['access_token']
        self._update_tokens()
