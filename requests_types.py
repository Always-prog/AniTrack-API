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
    season_id: int
    watch_datetime: str
    episode_order: int
    duration: int
    watched_time: int
    translate_type: str
    comment: Union[str, None]
    site: str


class SeasonCreate(BaseModel):
    season_name: Union[str, None]
    title_name: str
    episodes_count: int
    watch_motivation: str
    site: str
    summary: Union[str, None]


class DeleteEpisode(BaseModel):
    id: int


class DeleteSeason(BaseModel):
    id: int


class DeleteTitle(BaseModel):
    title_name: str


class UpdateSeason(BaseModel):
    id: int
    updated_fields: dict


class UpdateTitle(BaseModel):
    title_name: str
    updated_fields: dict

