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
            'title_name': self.title_name,
            'watch_motivation': self.watch_motivation,
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
            'season_name': self.season_name,
            'episodes_count': self.episodes_count,
            'watch_motivation': self.watch_motivation,
            'summary': self.summary,
            'season_order': self.season_order,
            'title': self.title.watch_motivation,
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
            'episode_name': self.episode_name,
            'season_name': self.season_name,
            'watch_date': self.watch_date.strftime('%Y-%m-%d'),
            'episode_order': self.episode_order,
            'episode_time': self.episode_time,
            'watched_time': self.watched_time,
            'translate_type': self.translate_type,
            'before_watch': self.before_watch,
            'after_watch': self.after_watch,
            'site': self.site
        }

# Base.metadata.create_all(engine)


