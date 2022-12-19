"""
Animes at Shikimori has the same MAL ID.
"""
from mal.types import MAL_TITLE_ID, MAL_TITLE_ID
from shikimori.client import ShikimoriClient


def get_anime_by_id(id: MAL_TITLE_ID):
    client = ShikimoriClient()
    response = client.anime(id)
    if response.status_code != 200:
        raise Exception('Response %s when getting anime from Shikimori ' % response.text)

    return response.json()


def get_franchise(id: MAL_TITLE_ID):
    client = ShikimoriClient()
    response = client.franchise(id)
    if response.status_code != 200:
        raise Exception('Response %s when getting franchise from Shikimori ' % response.text)
    return response.json()


def get_source_title(id: MAL_TITLE_ID) -> dict or None:  # TODO: Better typing
    nodes = get_franchise(id)['nodes']
    if nodes:
        return nodes[-1]


def get_source_title_id(id: MAL_TITLE_ID):
    source_title = get_source_title(id)
    if source_title is not None:
        return source_title['id']
    return id
