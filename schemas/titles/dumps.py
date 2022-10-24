from sqlalchemy import asc, func
from sqlalchemy.orm import Session
from database.tables import Title, Season, Episode


def to_file(db: Session, filepath: str):
    file_content = []
    space = '   '

    def new_episode(episode: Episode):
        if episode.before_watch:
            file_content.append(f'{space}{episode.before_watch}\n')
        file_content.append(f'{space}Серия {episode.episode_order},'
                            f' посмотрел {episode.watched_time} из {episode.episode_time}\n')
        if episode.after_watch:
            file_content.append(f'{space}{episode.after_watch}\n')

    def new_season(season_name):
        file_content.append(f'\n{space}Начал сезон {season_name}\n')

    def new_title(title_name):
        file_content.append(f'\n\n\n - [{title_name}]\n')

    last_title = None
    for season in db.query(Season).join(Episode).group_by(Season.season_name).order_by(func.min(Episode.watch_date)):
        season.episodes.sort(key=lambda ep: ep.episode_order)
        if last_title != season.title_name:
            new_title(season.title_name)

        new_season(season.season_name)
        for episode in season.episodes:
            new_episode(episode)

        last_title = season.title_name

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(''.join(file_content))


"""
Some saved queries

Getting watched titles order by watch 
db.query(Title).join(Season, Season.title_name == Title.title_name
).join(Episode, Episode.season_name == Season.season_name
).group_by(Title.title_name).order_by(func.min(Episode.watch_date)).all
"""
