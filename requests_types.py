from pydantic import BaseModel
from typing import Union


class Search(BaseModel):
    search: str


class SearchInTitle(BaseModel):
    title_name: str
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
    site: str


class SeasonCreate(BaseModel):
    season_name: Union[str, None]
    title_name: str
    episodes_count: int
    watch_motivation: str
    site: str
    summary: Union[str, None]


class DeleteEpisode(BaseModel):
    episode_name: str


class DeleteSeason(BaseModel):
    season_name: str


class DeleteTitle(BaseModel):
    title_name: str


class UpdateSeason(BaseModel):
    season_name: str
    updated_fields: dict


class UpdateTitle(BaseModel):
    title_name: str
    updated_fields: dict

