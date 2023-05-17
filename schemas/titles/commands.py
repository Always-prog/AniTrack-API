from sqlalchemy.orm import Session

from database.tables import Title
from mal.types import TITLE_NAME
from mal.utils import get_title_by_id
from shikimori.functions import get_source_title
from .exceptions import TitleNotFound


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


def create_title(db: Session, title_name: str, title_source: str,
                 title_source_id: int = None):
    title = Title(
        title_name=title_name,
        title_source=title_source,
        source_id=title_source_id
    )
    db.add(title)
    db.commit()
    db.refresh(title)
    return title


def prepare_source_title_name(title_name: TITLE_NAME):
    if ': ' in title_name:
        return title_name.split(':')[0]
    return title_name


def create_title_from_mal(db: Session, title_id: int):
    source = 'mal'
    source_title = get_source_title(title_id)
    if source_title is None:
        title_name = get_title_by_id(title_id)['title']
    else:
        title_name = source_title['name']

    return create_title(db=db, title_name=prepare_source_title_name(title_name), title_source=source,
                        title_source_id=title_id)
