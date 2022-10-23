from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from database.tables import Title, Episode
from .exceptions import TitleAlreadyExists

from ..seasons.commands import get_season

from fuzzywuzzy import process


def get_titles(db: Session) -> List[Title]:
    return db.query(Title).all()


def search_titles(db: Session, string: str):
    return db.query(Title).filter(Title.title_name.ilike(f'%{string}%'))


def get_recent_watched_episode(db: Session):
    return db.query(Episode).order_by(desc('watch_date'), desc('episode_order')).first()


def get_most_like_title(db: Session, search: str):
    title_name = process.extractOne(search, [title.title_name for title in get_titles(db)])[0]
    return get_title(db, title_name)


def get_most_like_season_in_title(db: Session, title_name: str, search: str):
    title = get_title(db, title_name)
    season_name = process.extractOne(search, [season.season_name for season in title.seasons])[0]

    return get_season(db, season_name)


def get_title(db: Session, title_name: str):
    return db.query(Title).filter_by(title_name=title_name).first()


def create_title(db: Session, title_name: str, watch_motivation: str):
    if get_title(db, title_name):
        raise TitleAlreadyExists(title_name)

    title = Title(
        title_name=title_name,
        watch_motivation=watch_motivation
    )
    db.add(title)
    db.commit()
    db.refresh(title)
    return title
