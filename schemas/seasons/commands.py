from sqlalchemy.orm import Session

from database.tables import Season
from mal.types import MAL_TITLE_ID
from mal.utils import get_title_by_id as mal_get_season_by_id
from schemas.episodes.commands import fill_season_with_episodes
from schemas.seasons.exceptions import SeasonNotFound
from shikimori.functions import get_anime_by_id as get_shikimori_anime_by_id


def get_season(db: Session, season_id: int):
    season = db.query(Season).filter_by(id=season_id).first()
    if season is None:
        raise SeasonNotFound(f'Season with id {season_id} don\'t exists')
    return season


def delete_season(db: Session, season_id: int):
    season = db.query(Season).filter_by(id=season_id).first()
    if season is None:
        raise SeasonNotFound(f'Season with id "{season_id}" don\'t exists!')
    db.delete(season)
    db.commit()


def create_season(db: Session,
                  season_name,
                  source_id,
                  title_id
                  ):
    season = Season(
        season_name=season_name,
        title_id=title_id,
        source_id=source_id
    )
    db.add(season)
    db.commit()

    return season


def refresh_episodes_in_season(db: Session, season: Season, title_id: MAL_TITLE_ID):
    mal_season_details = mal_get_season_by_id(title_id)
    episodes_count = mal_season_details['num_episodes']
    if episodes_count == 0:  # That means that title is not finished, and MAL doesn't published aried eps
        shikimori_title = get_shikimori_anime_by_id(title_id)
        episodes_count = shikimori_title['episodes_aired']

    average_episode_duration = mal_season_details['average_episode_duration']
    fill_season_with_episodes(db, season, episodes_count, average_episode_duration)


def create_season_from_mal(db: Session, title_id: int, mal_season_id: int):
    mal_season_details = mal_get_season_by_id(mal_season_id)
    season_name = mal_season_details['title']
    season = create_season(db, season_name=season_name, title_id=title_id, source_id=mal_season_id)
    refresh_episodes_in_season(db, season, mal_season_id)
    return season
