from typing import Tuple

from mal.client import MALClient
from mal.types import TITLE_ID, FRANCHISE_NAME, MAL_TITLE_ID, TITLE_NAME, FRANCHISE_CODE, MAL_TITLE_ID
from shikimori.functions import get_anime_by_id

def get_id(anime: dict):
    return anime.get('id', None) or anime['node']['id']


def get_name(anime: dict):
    return anime.get('title', None) or anime['node']['title']


# TODO: Add title type. Dict structure.
def get_title_by_id(id: TITLE_ID):
    client = MALClient()
    return client.get_anime_details(id)


def get_franchise_from_title(id: MAL_TITLE_ID) -> Tuple[FRANCHISE_NAME or None, FRANCHISE_CODE or None]:
    """
    Getting title name of the anime.
    :return:
    """

    anime = get_anime_by_id(id)
    code = anime['franchise']
    if code is None:
        return None, None
    return ''.join(x.capitalize()+' ' or '_' for x in code.split('_'))[:-1], code
