from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from . import Base, engine


class Title(Base):
    __tablename__ = "titles"

    title_name = Column(String(255), primary_key=True, index=True)
    watch_motivation = Column(Text)
    seasons = relationship("Season")

    def to_json(self):
        return {
            'titleName': self.title_name,
            'watchMotivation': self.watch_motivation,
        }


class Season(Base):
    __tablename__ = "seasons"

    season_name = Column(String(255), primary_key=True)
    title_name = Column(String(255), ForeignKey('titles.title_name'))
    title = relationship("Title", foreign_keys=[title_name], cascade="all, delete")
    episodes_count = Column(Integer)
    watch_motivation = Column(Text)
    summary = Column(Text)
    season_order = Column(Integer)
    episodes = relationship("Episode")

    def to_json(self):
        return {
            'seasonName': self.season_name,
            'episodeCount': self.episodes_count,
            'watchMotivation': self.watch_motivation,
            'summary': self.summary,
            'seasonOrder': self.season_order,
            'title': self.title.to_json()
        }


class Episode(Base):
    __tablename__ = "episodes"

    episode_name = Column(String(255), primary_key=True, nullable=True)
    season_name = Column(String(255), ForeignKey('seasons.season_name'))
    season = relationship("Season", foreign_keys=[season_name], cascade="all, delete")
    watch_date = Column(Date)
    episode_order = Column(Integer)
    episode_time = Column(Integer)
    watched_time = Column(Integer)
    translate_type = Column(String(255))
    before_watch = Column(Text, nullable=True)
    after_watch = Column(Text, nullable=True)
    site = Column(String(255), nullable=True)

    def to_json(self):
        return {
            'episodeName': self.episode_name,
            'watchDate': self.watch_date.strftime('%Y-%m-%d'),
            'episodeOrder': self.episode_order,
            'episodeTime': self.episode_time,
            'watchedTime': self.watched_time,
            'translateType': self.translate_type,
            'beforeWatch': self.before_watch,
            'afterWatch': self.after_watch,
            'site': self.site,
            'season': self.season.to_json()
        }

# Base.metadata.create_all(engine)


