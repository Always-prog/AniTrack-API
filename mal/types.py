from typing import Literal, List

TITLE_FIELD = Literal[
    'id', 'title', 'main_picture', 'start_date', 'end_date', 'synopsis',
    'mean', 'rank', 'popularity', 'num_list_users', 'num_scoring_users',
    'nsfw', 'genres', 'created_at', 'updated_at', 'status',
    'num_episodes', 'start_season', 'broadcast', 'source', 'average_episode_duration',
    'rating', 'studios', 'pictures', 'related_anime', 'related_manga', 'recommendations', 'statistics']
TITLE_FIELDS = List[TITLE_FIELD]

TITLE_NAME = str
TITLE_ID = int
MAL_TITLE_ID = int
FRANCHISE_NAME = str
FRANCHISE_CODE = str
