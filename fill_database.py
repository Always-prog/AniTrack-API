from database.tables import Title, Season, Episode, Record, Comment, User
from database import SessionLocal
from mal.client import MALClient
from datetime import datetime
import yaml
import re
import pandas as pd

SEASON_SUMMARY_SPLIT = '---'
DATE_FORMAT = '%m/%d/%Y'
RAW = str  # Raw data type
PARSED_RAW = dict  # Parsed data type


class ParserV3:
    def __init__(self, file_path: str, expand_episodes: bool = True):
        self.file_path = file_path
        self.file: PARSED_RAW = yaml.load(open(file_path, 'r', encoding='utf-8'))
        self.expand_episodes = expand_episodes

    def get_titles(self):
        return [
            {'title_name': title_name,
             'summary': title.get('summary'),
             'seasons': self.get_seasons(title)
             }
            for title_name, title in self.file.items()
        ]

    def get_seasons(self, title: PARSED_RAW):
        """
        [
        {
        'season_name': <season_name>
        'summary': <season_summary>,
        }
        ...
        ]
        """
        seasons = []
        is_first_key = True
        for season_name, season_raw in title.items():
            if is_first_key and season_name == 'summary':
                is_first_key = False
                continue
            season = self._parse_raw_season(season_raw)

            seasons.append({
                'season_name': season_name,
                'summary': season.get('summary'),
                'episodes_count': season['episodes_count'],
                'episodes': self.get_episodes(season)
            })

        return seasons

    def get_episodes(self, season: PARSED_RAW):
        """
        :param: expand: Expand every episode
        [
        {
        'date': <watching_date>
        'episodes': [
            {'order': <episode order>, 'duration': <None or int>, 'watched': <None or int>}
        ]
        }
        ...
        ]
        """
        episodes = []
        for index, record in enumerate(season['episodes_raw']):
            date = self._get_date(record)
            orders = self._get_orders(record)
            comment = self._get_comment(record)

            duration = None
            watched = None
            if self.expand_episodes:
                for order in orders:
                    episodes.append(self._create_episode(date, order, duration=duration, watched=watched))
                episodes[-1]['comment'] = comment
            else:
                episodes.append(self._create_episode(date, orders, comment, duration=duration, watched=watched))
        return episodes

    def _get_comment(self, record: RAW):
        comment = None
        if self._is_any_episode_recorded(record):
            date_and_orders = re.findall('\(.*?\)', record)
            comment = record.replace(date_and_orders[0], '', 1).replace(date_and_orders[1],'', 1)
        return comment

    def _get_date(self, record: RAW):
        try:
            date_raw = re.findall('\((.*?)\)', record)[0]
        except IndexError as e:
            raise ValueError(f'Not found date in record `{record}`')

        return datetime.strptime(date_raw, DATE_FORMAT)

    def _get_orders(self, record: RAW):
        try:
            orders_raw = re.findall('\((.*?)\)', record)[1]
        except IndexError as e:
            raise ValueError(f'Not found orders recorded in record `{record}`')

        return [int(i) for i in orders_raw.split(',') if i != '']

    def _is_any_episode_recorded(self, episode: RAW):
        if len(re.findall('\(.*?\)', episode)) >= 2:
            return True
        return False

    def _create_episode(self, date: datetime, orders: list[int] or int, comment: str = None, duration: int = None,
                        watched: int = None):
        return {
            'order': orders,
            'date': date,
            'comment': comment,
            'duration': duration,
            'watched': watched
        }

    def _parse_raw_season(self, season_raw: RAW):
        season = {
            'summary': season_raw.split(SEASON_SUMMARY_SPLIT)[0].replace(re.findall('\(.*?\)', season_raw)[0], '', 1),
            'episodes_count': int(re.findall('\((.*?)\)', season_raw)[0]),
            'episodes_raw': season_raw.split(SEASON_SUMMARY_SPLIT)[1:]
        }
        if season['episodes_raw'][-1].replace(' ', '').replace('\n', '') == '':
            season['episodes_raw'].pop(-1)
        return season


db = SessionLocal()
parser = ParserV3('listv3.yaml')

def fill():
    for title in parser.get_titles():
        title_name = title['title_name']
        title_summary = title['summary']
        seasons = title['seasons']
        _title = Title(
            title_name=title_name,
            summary=title_summary
        )
        db.add(_title)
        db.commit()
        for season in seasons:
            season_name = season['season_name']
            season_summary = season['summary']
            season_episodes_count = season['episodes_count']
            _season = Season(
                title_name=title_name,
                season_name=season_name,
                summary=season_summary,
                episodes_count=season_episodes_count
            )
            db.add(_season)
            db.commit()
            for episode in season['episodes']:
                order = episode['order']
                watch_date = episode['date']
                comment = episode['comment']

                _episode = Episode(
                    episode_name=f'{title_name}-{season_name} - ({order})',
                    watched_datetime=watch_date,
                    season_id=_season.id,
                    comment=comment,
                    translate_type='undefined'
                )
                db.add(_episode)
                db.commit()


def update_order():
    for title in parser.get_titles():
        title_name = title['title_name']
        title_summary = title['summary']
        seasons = title['seasons']
        _title = db.query(Title).filter_by(
            title_name=title_name
        ).first()
        for season in seasons:
            season_name = season['season_name']
            season_summary = season['summary']
            season_episodes_count = season['episodes_count']
            _season = db.query(Season).filter_by(
                season_name=season_name,
            ).first()
            for episode in season['episodes']:
                order = episode['order']
                watch_date = episode['date']
                comment = episode['comment']
                if title_name == 'Neverland' and season_name == 'Season 2':
                    _episode = Episode(
                        episode_name=f'{title_name}-{season_name} - ({order})',
                        watched_datetime=watch_date,
                        comment=comment,
                        episode_order=order,
                        season_id=_season.id,
                    )
                    print(order)
                    _episode.episode_order = order
                    db.add(_episode)
                    db.commit()


def export_episodes():
    episodes = []
    for ep in db.query(Episode).all():
        episodes.append({
        'episode_name': ep.episode_name,
        'season_id': ep.season_id,
        'season': ep.season,
        'watched_datetime': ep.watched_datetime,
        'episode_order': ep.episode_order,
        'duration': ep.duration,
        'watched_time': ep.watched_time,
        'translate_type': ep.translate_type,
        'comment': ep.comment,
        'site': ep.site
        })
    import json
    with open('episodes-11-22-2022.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(episodes, indent=3, ensure_ascii=False, default=str))

import json
def load_episodes_and_fill_records():
    episodes = json.load(open('episodes-11-22-2022.json', 'r', encoding='utf-8'))
    for ep in episodes:
        print(ep)
        _episode = Episode(
            episode_name=ep['episode_name'],
            season_id=ep['season_id'],
            episode_order=ep['episode_order'],
            duration=ep['duration']
        )
        db.add(_episode)
        db.commit()
        _record = Record(
            episode_id=_episode.id,
            watched_from = 0,
            watched_time = ep['watched_time'],
            watched_datetime = ep['watched_datetime'],
            translate_type = ep['translate_type'],
            site = ep['site']
        )
        db.add(_record)
        db.commit()
        if (ep['comment']):
            _comment = Comment(
                episode_id=_episode.id,
                text=ep['comment'],
                comment_datetime=ep['watched_datetime']
            )
            db.add(_comment)
            db.commit()


def fill_no_exists_episodes():
    for season in db.query(Season).all():
        if len(season.episodes) < season.episodes_count:
            print(f'For {season.title_name} - {season.season_name}({len(season.episodes)}): ', end='')
            eps = [ep.episode_order for ep in season.episodes]
            for ep_order in range(1, season.episodes_count+1):
                if ep_order not in list(eps) and len(season.episodes):
                    print(f'{ep_order}, ',end='')
                    _episode = Episode(
                        episode_name=f'{season.title_name}-{season.season_name} - ({ep_order})',
                        season_id=season.id,
                        episode_order=ep_order,
                        duration=season.episodes[-1].duration
                    )
                    db.add(_episode)
                    db.commit()
            print()




def export_titles_seasons_episodes_records_comments():
    titles = []
    for title in db.query(Title).all():
        titles.append(dict(
            id = title.id,
            title_name = title.title_name,
            title_type = title.title_type,
            watch_motivation = title.watch_motivation,
            summary = title.summary,
        ))
    with open('titles-11-26-2022.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(titles, indent=3, ensure_ascii=False))
    return

    seasons = []
    for season in db.query(Season).all():
        seasons.append(dict(
            id=season.id,
            season_name = season.season_name,
            title_id = season.title.id,
            episodes_count = season.episodes_count,
            watch_motivation = season.watch_motivation,
            primary_site = season.primary_site,
            summary = season.summary
        ))
    with open('seasons-11-26-2022.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(seasons, indent=3, ensure_ascii=False, default=str))

    episodes = []
    for episode in db.query(Episode).all():
        episodes.append(dict(
            id=episode.id,
            episode_name = episode.episode_name,
            season_id = episode.season_id,
            episode_order = episode.episode_order,
            duration = episode.duration,
        ))
    with open('episodes-11-26-2022.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(episodes, indent=3, ensure_ascii=False, default=str))

    records = []
    for record in db.query(Record).all():
        records.append(dict(
            id=record.id,
            episode_id=record.episode_id,
            watched_from = record.watched_from,
            watched_time = record.watched_time,
            comment = record.comment,
            watched_datetime = record.watched_datetime,
            translate_type = record.translate_type,
            site = record.site,
        ))
    with open('records-11-26-2022.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(records, indent=3, ensure_ascii=False, default=str))

    comments = []
    for comment in db.query(Comment).all():
        comments.append(dict(
            id=comment.id,
            episode_id = comment.episode_id,
            text = comment.text,
            comment_datetime = comment.comment_datetime
        ))
    with open('comments-11-26-2022.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(comments, indent=3, ensure_ascii=False, default=str))

def import_titles_from_json_11_24_2022():
    with open('titles-11-24-2022.json', 'r', encoding='utf-8') as f:
        titles = json.loads(f.read())
    for title in titles:
        _title = Title(
            id = title['id'],
            title_name = title['title_name'],
            title_datasource = 'manually',
            title_type = title['title_type'],
            watch_motivation = title['watch_motivation'],
            summary = title['summary'],
        )
        db.add(_title)
        db.commit()


def import_seasons_from_json_11_24_2022():
    with open('seasons-11-24-2022.json', 'r', encoding='utf-8') as f:
        seasons = json.loads(f.read())

    for season in seasons:
        _season = Season(
            id=season['id'],
            season_name=season['season_name'],
            title_id=season['title_id'],
            episodes_count=season['episodes_count'],
            watch_motivation=season['watch_motivation'],
            primary_site=season['primary_site'],
            summary=season['summary']
        )
        db.add(_season)
        db.commit()

def import_episodes_from_json_11_24_2022():
    with open('episodes-11-24-2022.json', 'r', encoding='utf-8') as f:
        episodes = json.loads(f.read())

    for episode in episodes:
        _episode = Episode(
            id=episode['id'],
            episode_name=episode['episode_name'],
            season_id=episode['season_id'],
            episode_order=episode['episode_order'],
            duration=episode['duration'],
        )
        db.add(_episode)
        db.commit()

def import_records_from_json_11_24_2022():
    with open('records-11-24-2022.json', 'r', encoding='utf-8') as f:
        records = json.loads(f.read())

    for record in records:
        _record = Record(
            id=record['id'],
            episode_id=record['episode_id'],
            watched_from=record['watched_from'],
            watched_time=record['watched_time'],
            comment=record['comment'],
            watched_datetime=record['watched_datetime'],
            translate_type=record['translate_type'],
            site=record['site'],
        )
        db.add(_record)
        db.commit()


def import_comments_from_json_11_24_2022():
    with open('comments-11-24-2022.json', 'r', encoding='utf-8') as f:
        comments = json.loads(f.read())

    for comment in comments:
        _comment = Comment(
            id=comment['id'],
            episode_id=comment['episode_id'],
            text=comment['text'],
            comment_datetime=comment['comment_datetime']
        )
        db.add(_comment)
        db.commit()

def import_all_from_json_12_04_2022():
    db = SessionLocal()
    user = db.query(User).filter_by(id=1).first()
    client = MALClient()
    with open('titles-11-24-2022.json', 'r', encoding='utf-8') as f:
        titles = json.load(f)

    with open('seasons-renamed-12-04-2022.json', 'r', encoding='utf-8') as f:
        seasons = json.load(f)

    with open('episodes-11-24-2022.json', 'r', encoding='utf-8') as f:
        episodes = json.load(f)

    with open('records-11-24-2022.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    with open('comments-11-24-2022.json', 'r', encoding='utf-8') as f:
        comments = json.load(f)

    for season in seasons:
        season_at_mal = client.search(season['season_name']).json()['data'][0]['node']
        source_id = season_at_mal['id']
        title_name = season_at_mal['title']

        for episode in episodes:
            if episode['season_id'] != season['id']:
                continue

            for record in records:
                if record['episode_id'] != episode['id']:
                    continue
                from schemas.records.commands import create_record_from_source
                create_record_from_source(
                    source='mal',
                    source_type='season',
                    source_id=source_id,
                    episode_order=episode['episode_order'],
                    watch_datetime=record['watched_datetime'],
                    watched_from=0,
                    watched_time=float(record['watched_time']) * 60,
                    translate_type=record['translate_type'],
                    comment=None,
                    site=record['site'],
                    db=db,
                    user=user
                )

            for comment in comments:
                if comment['episode_id'] != episodes['id']:
                    continue
                # print(comment['text'])
        break

import_all_from_json_12_04_2022()