from sqlalchemy import desc

from database.tables import Episode
from sqlalchemy.orm import Session

from settings import EPISODES_TXT_FILE_PATH, DUMP_SCRIPT_PATH
from .utils import generate_episode_name
from .exceptions import EpisodeAlreadyExists, EpisodeNotFound
from schemas.episodes.dumps import dump_database, write_episodes_to_txt
from ..seasons.commands import get_season


def find_season_episode_by_order(db: Session, season_id, episode_order):
    return db.query(Episode).filter_by(
        season_id=season_id,
        episode_order=episode_order
    ).first()


def find_episode_by_name(db: Session, episode_name):
    return db.query(Episode).filter_by(
        episode_name=episode_name
    ).first()


def get_episodes_by_site(db: Session, site: str):
    return db.query(Episode).filter_by(
        site=site
    ).order_by(desc('watch_date'), desc('episode_order'))


def delete_episode(db: Session, episode_id: int):
    episode = db.query(Episode).filter_by(id=episode_id).first()
    if episode is None:
        raise EpisodeNotFound(f'Episode with id "{episode_id}" not found!')

    db.delete(episode)
    db.commit()


def dump_episodes(db: Session):
    write_episodes_to_txt(db, EPISODES_TXT_FILE_PATH)
    dump_database(DUMP_SCRIPT_PATH)


def create_episode(db: Session,
                   season_id: int,
                   watch_datetime,
                   episode_order,
                   duration,
                   watched_time,
                   translate_type,
                   episode_name=None,
                   comment=None,
                   site=None
                   ):
    season = get_season(db, season_id)
    if not episode_name:
        episode_name = generate_episode_name(season.title_name, season.season_name, episode_order)

    if find_season_episode_by_order(db, season.id, episode_order):
        raise EpisodeAlreadyExists(f'Episode in {season.title_name} {season.season_name} with order {episode_order} already exists.')

    episode = Episode(
        episode_name=episode_name,
        season_id=season_id,
        watched_datetime=watch_datetime,
        episode_order=episode_order,
        duration=duration,
        watched_time=watched_time,
        translate_type=translate_type,
        comment=comment,
        site=site,
    )
    db.add(episode)
    db.commit()
    db.refresh(episode)
    return episode
