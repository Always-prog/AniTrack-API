from typing import List

from sqlalchemy.orm import Session

from database.tables import Title
from .exceptions import TitleAlreadyExists


def get_titles(db: Session) -> List[Title]:
    return db.query(Title).all()


def search_titles(db: Session, string: str):
    return db.query(Title).filter(Title.title_name.ilike(f'%{string}%'))


def get_title(db: Session, title_name: str):
    return db.query(Title).filter(Title.title_name.ilike(title_name)).first()


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
