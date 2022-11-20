from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Numeric
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

    id = Column(Integer, primary_key=True, index=True)
    season_name = Column(String(255))
    title_name = Column(String(255), ForeignKey('titles.title_name'))  # TODO: Cascade
    title = relationship("Title", foreign_keys=[title_name])
    episodes_count = Column(Integer)
    watch_motivation = Column(Text, nullable=True)
    primary_site = Column(String(255))
    summary = Column(Text)
    episodes = relationship("Episode", cascade="all, delete-orphan")

    def to_json(self, include_title=True):
        return {
            'id': self.id,
            'seasonName': self.season_name,
            'episodeCount': self.episodes_count,
            'watchMotivation': self.watch_motivation,
            'summary': self.summary,
            'title': self.title.to_json() if include_title else None,
            'episodes': [ep.to_json(include_season=False) for ep in self.episodes],
        }


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    episode_name = Column(String(255), nullable=True)
    season_id = Column(Integer, ForeignKey('seasons.id'))
    season = relationship("Season", foreign_keys=[season_id])
    watched_datetime = Column(DateTime)
    episode_order = Column(Integer)
    duration = Column(Numeric)
    watched_time = Column(Numeric)
    translate_type = Column(String(255))
    comment = Column(Text, nullable=True)
    site = Column(String(255), nullable=True)

    def to_json(self, include_season=True):
        return {
            'id': self.id,
            'episodeName': self.episode_name,
            'watchDate': self.watched_datetime.strftime('%Y-%m-%d'),
            'episodeOrder': self.episode_order,
            'episodeTime': self.duration,
            'watchedTime': self.watched_time,
            'translateType': self.translate_type,
            'comment': self.comment,
            'season': self.season.to_json() if include_season else None,
            'site': self.site
        }

# Base.metadata.create_all(engine)


