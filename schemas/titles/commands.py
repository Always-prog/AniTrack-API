from sqlalchemy.orm import Session

from database.tables import Title
from mal.utils import get_title_by_id as mal_get_title_by_id, get_global_title_name as mal_get_global_title_name
from .exceptions import TitleAlreadyExists, TitleNotFound


def get_title(db: Session, title_name: str):
    title = db.query(Title).filter_by(title_name=title_name).first()
    if title is None:
        raise TitleNotFound(f'Title with name "{title_name}" not found!')
    return title


def delete_title(db: Session, title_name: str):
    title = db.query(Title).filter_by(title_name=title_name).first()
    if title is None:
        raise TitleNotFound(f'Title with name "{title_name}" not found!')
    db.delete(title)
    db.commit()


def create_title(db: Session, title_name: str, title_source: str, title_source_id: int):
    title = Title(
        title_name=title_name,
        title_source=title_source,
        source_id=title_source_id
    )
    db.add(title)
    db.commit()
    db.refresh(title)
    return title


def create_title_from_mal(db: Session, title_id: int):
    source = 'mal'
    title_details = mal_get_title_by_id(title_id)
    title_name = mal_get_global_title_name(title_details['title'])
    return create_title(db, title_name, source, title_id)
