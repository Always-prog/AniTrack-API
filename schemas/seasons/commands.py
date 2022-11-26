from sqlalchemy.orm import Session

from database.tables import Season
from mal.utils import get_title_by_id as mal_get_season_by_id
from schemas.episodes.commands import fill_season_with_episodes
from schemas.seasons.exceptions import SeasonNotFound


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


def refresh_episodes_from_mal(db: Session, season: Season, mal_season_id: int):
    mal_season_details = mal_get_season_by_id(mal_season_id)
    episodes_count = mal_season_details['num_episodes']
    average_episode_duration = mal_season_details['average_episode_duration']
    fill_season_with_episodes(db, season, episodes_count, average_episode_duration)


def create_season_from_mal(db: Session, title_id: int, mal_season_id: int):
    mal_season_details = mal_get_season_by_id(mal_season_id)
    season_name = mal_season_details['title']
    season = create_season(db, season_name=season_name, title_id=title_id, source_id=mal_season_id)
    refresh_episodes_from_mal(db, season, mal_season_id)
    return season
