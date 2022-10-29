from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from . import Base, engine


class Title(Base):
    __tablename__ = "titles"

    title_name = Column(String(255), primary_key=True, index=True)
    title_type = Column(String(255), nullable=True)
    watch_motivation = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    seasons = relationship("Season", cascade="all, delete-orphan")

    def to_json(self):
        return {
            'titleName': self.title_name,
            'watchMotivation': self.watch_motivation,
            'summary': self.summary,
            'seasons': [season.to_json(include_title=False) for season in self.seasons]
        }


class Season(Base):
    __tablename__ = "seasons"

    season_name = Column(String(255), primary_key=True)
    title_name = Column(String(255), ForeignKey('titles.title_name'))  # TODO: Cascade
    title = relationship("Title", foreign_keys=[title_name])
    episodes_count = Column(Integer)
    watch_motivation = Column(Text, nullable=True)
    primary_site = Column(String(255))
    summary = Column(Text)
    episodes = relationship("Episode", cascade="all, delete-orphan")

    def to_json(self, include_title=True):
        return {
            'seasonName': self.season_name,
            'episodeCount': self.episodes_count,
            'watchMotivation': self.watch_motivation,
            'summary': self.summary,
            'title': self.title.to_json() if include_title else None,
            'episodes': [ep.to_json(include_season=False) for ep in self.episodes],
        }


class Episode(Base):
    __tablename__ = "episodes"

    episode_name = Column(String(255), primary_key=True, nullable=True)
    season_name = Column(String(255), ForeignKey('seasons.season_name'))
    season = relationship("Season", foreign_keys=[season_name])
    watch_date = Column(Date)
    episode_order = Column(Integer)
    episode_time = Column(Integer)
    watched_time = Column(Integer)
    translate_type = Column(String(255))
    before_watch = Column(Text, nullable=True)
    after_watch = Column(Text, nullable=True)
    site = Column(String(255), nullable=True)

    def to_json(self, include_season=True):
        return {
            'episodeName': self.episode_name,
            'watchDate': self.watch_date.strftime('%Y-%m-%d'),
            'episodeOrder': self.episode_order,
            'episodeTime': self.episode_time,
            'watchedTime': self.watched_time,
            'translateType': self.translate_type,
            'beforeWatch': self.before_watch,
            'afterWatch': self.after_watch,
            'season': self.season.to_json() if include_season else None,
            'site': self.site
        }

# Base.metadata.create_all(engine)


