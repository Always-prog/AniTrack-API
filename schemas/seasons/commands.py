from typing import List

from fuzzywuzzy import process
from sqlalchemy import desc
from sqlalchemy.orm import Session

from database.tables import Season, Title, Episode
from schemas.seasons.exceptions import SeasonAlreadyExists, SeasonDontExists


def generate_season_name(title_name, season_order):
    return f'{title_name} season {season_order}'


def find_season_by_order(db: Session, title_name, season_order):
    return db.query(Season).filter_by(
        title_name=title_name,
        season_order=season_order
    ).first()


def find_season_by_name(db: Session, season_name):
    return db.query(Season).filter_by(
        season_name=season_name,
    ).first()


def get_season(db: Session, season_name: str):
    return db.query(Season).filter_by(season_name=season_name).first()


def get_season_watched_episodes(db: Session, season_name: str):
    if not find_season_by_name(db, season_name):
        raise SeasonDontExists(f'Season {season_name} don\'t exists!')
    return db.query(Episode).filter_by(season_name=season_name).order_by(desc('watch_date'), desc('episode_order'))


def get_most_like_season(db: Session, search: str):
    season_name = process.extractOne(search, [season.season_name for season in get_seasons(db)])[0]
    return get_season(db, season_name)


def get_seasons(db: Session) -> List[Season]:
    return db.query(Season).all()


def create_season(db: Session,
                  title_name,
                  episodes_count,
                  watch_motivation,
                  season_order,
                  summary=None,
                  season_name=None
                  ):
    if season_name is None:
        season_name = generate_season_name(title_name, season_order)

    if find_season_by_name(db, season_name):
        raise SeasonAlreadyExists(f'Season with name {season_name} already exists')

    if find_season_by_order(db, title_name, season_order):
        raise SeasonAlreadyExists(f'Season with order {season_order} in {title_name} already exists')

    season = Season(
        season_name=season_name,
        title_name=title_name,
        episodes_count=episodes_count,
        watch_motivation=watch_motivation,
        summary=summary,
        season_order=season_order
    )
    db.add(season)
    db.commit()
    db.refresh(season)
    return season
