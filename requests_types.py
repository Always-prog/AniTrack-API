from pydantic import BaseModel
from typing import Union


class TitleSearch(BaseModel):
    search: str


class TitleCreate(BaseModel):
    title_name: str
    watch_motivation: str


class EpisodeCreate(BaseModel):
    episode_name: Union[str, None]
    season_name: str
    watch_date: str
    episode_order: int
    episode_time: int
    watched_time: int
    translate_type: str
    before_watch: Union[str, None]
    after_watch: Union[str, None]
    site: Union[str, None]


class SeasonCreate(BaseModel):
    season_name: Union[str, None]
    title_name: str
    episodes_count: int
    watch_motivation: str
    summary: Union[str, None]
    season_order: int
