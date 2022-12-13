"""
Animes at Shikimori has the same MAL ID.
"""
from mal.types import GLOBAL_TITLE_ID
from shikimori.client import ShikimoriClient


def get_anime_by_id(id: GLOBAL_TITLE_ID):
    client = ShikimoriClient()
    response = client.anime(id)
    if response.status_code != 200:
        raise Exception('Response %s when getting anime from Shikimori ' % response.text)

    return response.json()
