from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Numeric
from sqlalchemy.orm import relationship
from . import Base, engine


class Title(Base):
    __tablename__ = "titles"

    id = Column(Integer, primary_key=True, index=True)
    title_source = Column(String(255))
    source_id = Column(Integer)
    title_name = Column(String(255), index=True)
    title_type = Column(String(255), nullable=True)
    seasons = relationship("Season", cascade="all, delete-orphan")

    def to_json(self):
        return {
            'titleName': self.title_name,
            'seasons': [season.to_json(include_title=False) for season in self.seasons]
        }


class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True, index=True)
    season_name = Column(String(255))
    source_id = Column(Integer, nullable=False)
    title_id = Column(Integer, ForeignKey('titles.id'))  # TODO: Cascade
    title = relationship("Title", foreign_keys=[title_id])
    episodes = relationship("Episode", cascade="all, delete-orphan")

    def to_json(self, include_title=True):
        return {
            'id': self.id,
            'seasonName': self.season_name,
            'title': self.title.to_json() if include_title else None,
            'episodes': [ep.to_json(include_season=False) for ep in self.episodes],
        }


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    episode_name = Column(String(255), nullable=True)
    season_id = Column(Integer, ForeignKey('seasons.id'))
    season = relationship("Season", foreign_keys=[season_id])
    episode_order = Column(Integer)
    duration = Column(Numeric)
    records = relationship("Record", cascade="all, delete-orphan")

    def to_json(self, include_season=True):
        return {
            'id': self.id,
            'seasonId': self.season_id,
            'episodeName': self.episode_name,
            'episodeOrder': self.episode_order,
            'duration': self.duration,
            'season': self.season.to_json() if include_season else None,
            'records': [r.to_json(include_episode=False) for r in self.records],
        }


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", foreign_keys=[owner_id])

    episode_id = Column(Integer, ForeignKey('episodes.id'))
    episode = relationship("Episode", foreign_keys=[episode_id])
    text = Column(Text, nullable=False)
    comment_datetime = Column(DateTime, nullable=True)

    def to_json(self, include_episode=True):
        return {
            'id': self.id,
            'episodeId': self.episode_id,
            'commentDatetime': self.watched_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'text': self.text,
            'episode': self.episode.to_json() if include_episode else None,
        }


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", foreign_keys=[owner_id])

    episode_id = Column(Integer, ForeignKey('episodes.id'))
    episode = relationship("Episode", foreign_keys=[episode_id])
    watched_from = Column(Numeric, nullable=False)
    watched_time = Column(Numeric, nullable=False)
    comment = Column(Text, nullable=True)
    watched_datetime = Column(DateTime)
    translate_type = Column(String(255))
    site = Column(String(255), nullable=True)

    def to_json(self, include_episode=True):
        return {
            'id': self.id,
            'episodeId': self.episode_id,
            'watchDatetime': self.watched_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'watchedTime': self.watched_time,
            'translateType': self.translate_type,
            'comment': self.comment,
            'episode': self.episode.to_json() if include_episode else None,
            'site': self.site,
        }


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    created_on = Column(DateTime)
    password = Column(String(255), nullable=False)
    disabled = Column(Boolean, default=False)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", foreign_keys=[user_id])


Base.metadata.create_all(engine)


