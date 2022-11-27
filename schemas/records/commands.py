from sqlalchemy import desc
from sqlalchemy.orm import Session

from schemas.episodes.exceptions import EpisodeNotFound
from schemas.records.exceptions import UnsupportedSource, UnsupportedSourceType
from mal.utils import get_global_title_from_title
from schemas.titles.commands import create_title_from_mal
from schemas.seasons.commands import create_season_from_mal, refresh_episodes_from_mal
from datetime import datetime
from database.tables import Record, Title, Season, Episode, User


def create_record_from_source(db: Session, user: User,
                              source: str,
                              source_type: str,
                              source_id: int,
                              episode_order: int,
                              watch_datetime: str,
                              watched_from: int or float,
                              watched_time: int or float,
                              translate_type: str,
                              site: str,
                              comment: str or None = None):
    #  Get the name and id of source
    if source != 'mal':
        raise UnsupportedSource('Unsupported source: %s' % source)
    if source_type != 'season':
        raise UnsupportedSourceType('Unsupported source type: %s' % source)
    #  Get the title of that season
    source_title_name, source_title_id = get_global_title_from_title(source_id)

    #  Check that title is exists
    title_db = db.query(Title).filter_by(source_id=source_title_id).first()
    if not title_db:
        title_db = create_title_from_mal(db, source_title_id)

    #  Check that season is exists (And create episodes)
    season_db = db.query(Season).filter_by(source_id=source_id).first()
    if not season_db:
        season_db = create_season_from_mal(db, title_db.id, source_id)

    #  Record record
    episode_db = db.query(Episode).filter_by(season_id=season_db.id, episode_order=episode_order).first()
    if not episode_db:
        # Refreshing season episodes
        refresh_episodes_from_mal(db, season=season_db, mal_season_id=source_id)
        episode_db = db.query(Episode).filter_by(season_id=season_db.id, episode_order=episode_order).first()

    if not episode_db:
        raise EpisodeNotFound(
            f'Episode not found: {season_db.title.title_name} -> {season_db.title.title_name} -> {episode_order}')
    return create_record(db, user, episode_db, watch_datetime, watched_from, watched_time, translate_type, comment, site)


def create_record(db: Session,
                  user: User,
                  episode: Episode,
                  watch_datetime: str or datetime,
                  watched_from: int,
                  watched_time: int,
                  translate_type: str,
                  comment: str = None,
                  site: str = None
                  ):
    record = Record(
        owner_id=user.id,
        episode_id=episode.id,
        watched_datetime=watch_datetime,
        watched_from=watched_from,
        watched_time=watched_time,
        translate_type=translate_type,
        comment=comment,
        site=site,
    )
    db.add(record)
    db.commit()
    return record
