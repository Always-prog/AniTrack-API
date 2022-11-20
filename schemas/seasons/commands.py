from typing import List

from fuzzywuzzy import process
from sqlalchemy import desc
from sqlalchemy.orm import Session

from database.tables import Season, Title, Episode
from schemas.seasons.exceptions import SeasonAlreadyExists, SeasonNotFound


def find_season_by_name(db: Session, season_name):
    return db.query(Season).filter_by(
        season_name=season_name,
    ).first()


def get_season(db: Session, season_id: int):
    season = db.query(Season).filter_by(id=season_id).first()
    if season is None:
        raise SeasonNotFound(f'Season with id {season_id} don\'t exists')
    return season


def update_season(db: Session, season_id: id, **kwargs):
    season = get_season(db, season_id)
    for column, value in kwargs.items():
        setattr(season, column, value)
    db.commit()
    return season


def get_season_watched_episodes(db: Session, season_id: int):
    if not get_season(db, season_id):
        raise SeasonNotFound(f'Season with id {season_id} don\'t exists!')
    return db.query(Episode).filter_by(id=season_id).order_by(desc('watch_date'), desc('episode_order'))


def get_most_like_season(db: Session, search: str):
    season_name = process.extractOne(search, [season.season_name for season in get_seasons(db)])[0]
    return get_season(db, season_name)


def get_seasons(db: Session) -> List[Season]:
    return db.query(Season).all()


def get_season_by_site(db: Session, site: str):
    primary = db.query(Season).filter_by(primary_site=site).first()
    if primary is not None:
        return primary
    secondary = db.query(Episode).filter_by(site=site).first()
    if secondary is not None:
        return secondary.season

    raise SeasonNotFound(f'Season by site "{site}" don\'t exists')


def delete_season(db: Session, season_id: int):
    season = db.query(Season).filter_by(id=season_id).first()
    if season is None:
        raise SeasonNotFound(f'Season with id "{season_id}" don\'t exists!')
    db.delete(season)
    db.commit()


def create_season(db: Session,
                  season_name,
                  title_name,
                  episodes_count,
                  watch_motivation,
                  primary_site,
                  summary=None,
                  ):
    if find_season_by_name(db, season_name):
        raise SeasonAlreadyExists(f'Season with name {season_name} already exists')

    season = Season(
        season_name=season_name,
        title_name=title_name,
        episodes_count=episodes_count,
        watch_motivation=watch_motivation,
        primary_site=primary_site,
        summary=summary
    )
    db.add(season)
    db.commit()
    db.refresh(season)
    return season
