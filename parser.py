from datetime import datetime
import yaml
import re

file = './example3.yaml'

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
