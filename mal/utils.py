from typing import Tuple

from mal.client import MALClient
from mal.types import TITLE_ID, GLOBAL_TITLE_NAME, GLOBAL_TITLE_ID, TITLE_NAME


def get_id(anime: dict):
    return anime.get('id', None) or anime['node']['id']


def get_name(anime: dict):
    return anime.get('title', None) or anime['node']['title']


# TODO: Add title type. Dict structure.
def get_title_by_id(id: TITLE_ID):
    client = MALClient()
    return client.get_anime_details(id)


def get_global_title_name(title_name: TITLE_NAME):
    """
    Return title name from title name, because title name may be just name of season.
    :return:
    """
    if ':' in title_name:
        return title_name.split(':')[0]

    return title_name


def get_global_title_from_title(id: TITLE_ID) -> Tuple[GLOBAL_TITLE_NAME, GLOBAL_TITLE_ID]:
    """
    Getting title name of the anime.
    :return:
    """
    client = MALClient()

    title = client.get_anime_details(id, ['related_anime', 'start_date'])
    related_anime = title['related_anime']
    prequels = [a for a in related_anime if a['relation_type'] == 'prequel']
    if not prequels:
        return get_global_title_name(title['title']), id

    prequels_sorted = sorted(prequels, key=lambda x: client.get_anime_details(id, ['start_date'])['start_date'])
    first_released_anime = prequels_sorted[0]['node']
    return get_global_title_name(first_released_anime['title']), first_released_anime['id']
