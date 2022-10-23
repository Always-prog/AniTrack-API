from sqlalchemy import desc

from database.tables import Episode
from sqlalchemy.orm import Session
from .utils import generate_episode_name
from .exceptions import EpisodeAlreadyExists


def find_season_episode_by_order(db: Session, season_name, episode_order):
    return db.query(Episode).filter_by(
        season_name=season_name,
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


def create_episode(db: Session,
                   season_name,
                   watch_date,
                   episode_order,
                   episode_time,
                   watched_time,
                   translate_type,
                   episode_name=None,
                   before_watch=None,
                   after_watch=None,
                   site=None
                   ):
    if not episode_name:
        episode_name = generate_episode_name(season_name, episode_order)

    if find_season_episode_by_order(db, season_name, episode_order):
        raise EpisodeAlreadyExists(f'Episode in {season_name} with order {episode_order} already exists.')

    if find_episode_by_name(db, episode_name):
        raise EpisodeAlreadyExists(f'Episode with name {episode_order} already exists.')

    episode = Episode(
        episode_name=episode_name,
        season_name=season_name,
        watch_date=watch_date,
        episode_order=episode_order,
        episode_time=episode_time,
        watched_time=watched_time,
        translate_type=translate_type,
        before_watch=before_watch,
        after_watch=after_watch,
        site=site,
    )
    db.add(episode)
    db.commit()
    db.refresh(episode)
    return episode
