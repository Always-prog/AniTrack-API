from sqlalchemy import desc

from database.tables import Episode, Season
from sqlalchemy.orm import Session

from settings import EPISODES_TXT_FILE_PATH, DUMP_SCRIPT_PATH
from .utils import generate_episode_name
from .exceptions import EpisodeAlreadyExists, EpisodeNotFound
from schemas.episodes.dumps import dump_database, write_episodes_to_txt
from schemas.seasons.exceptions import SeasonNotFound


def find_season_episode_by_order(db: Session, season_id, episode_order):
    return db.query(Episode).filter_by(
        season_id=season_id,
        episode_order=episode_order
    ).first()


def dump_episodes(db: Session):
    write_episodes_to_txt(db, EPISODES_TXT_FILE_PATH)
    dump_database(DUMP_SCRIPT_PATH)


def create_episode(db: Session,
                   season: Season,
                   episode_order,
                   duration,
                   ):
    episode_name = generate_episode_name(season.title.title_name, season.season_name, episode_order)

    if find_season_episode_by_order(db, season.id, episode_order):
        raise EpisodeAlreadyExists(
            f'Episode in {season.title_name} {season.season_name} with order {episode_order} already exists.')

    episode = Episode(
        episode_name=episode_name,
        season_id=season.id,
        episode_order=episode_order,
        duration=duration
    )
    db.add(episode)
    db.commit()
    return episode


def fill_season_with_episodes(db: Session, season: Season, episodes_count: int, avg_duration: int):
    already_exists_episodes = [ep.episode_order for ep in season.episodes]
    episodes = []

    for ep_order in range(1, episodes_count + 1):
        if ep_order not in already_exists_episodes:
            episodes.append(create_episode(db, season=season, episode_order=ep_order, duration=avg_duration))
    return episodes
