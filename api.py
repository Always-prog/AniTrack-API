from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database.sessions import get_db
from schemas.episodes.exceptions import EpisodeAlreadyExists
from schemas.episodes.commands import create_episode, get_episodes_by_site
from schemas.seasons.commands import get_seasons, create_season, get_most_like_season, get_season, \
    get_season_watched_episodes
from schemas.seasons.exceptions import SeasonAlreadyExists, SeasonDontExists, SeasonNoOneWatchedEpisode
from schemas.titles.commands import get_titles, search_titles, create_title, get_most_like_title, \
    get_most_like_season_in_title, get_recent_watched_episode
from schemas.titles.exceptions import TitleAlreadyExists
from requests_types import Search, TitleCreate, EpisodeCreate, SeasonCreate, SearchInTitle
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/titles")
async def all_titles_endpoint(db: Session = Depends(get_db)):
    titles = get_titles(db)
    return [title.to_json() for title in titles]


@app.get("/search/titles")
async def search_titles_endpoint(search: str, db: Session = Depends(get_db)):
    titles = search_titles(db, search)
    return [title.title_name for title in titles]


@app.post("/title/create")
async def create_title_endpoint(data: TitleCreate, db: Session = Depends(get_db)):
    try:
        title = create_title(db, data.title_name, data.watch_motivation)
    except TitleAlreadyExists as e:
        raise HTTPException(status_code=409, detail=e.__str__())
    return title.to_json()


@app.get("/seasons")
async def all_seasons_endpoint(db: Session = Depends(get_db)):
    seasons = get_seasons(db)
    return [season.to_json() for season in seasons]


@app.post("/episode/create")
async def create_episode_endpoint(data: EpisodeCreate, db: Session = Depends(get_db)):
    try:
        episode = create_episode(
            season_name=data.season_name,
            watch_date=data.watch_date,
            episode_order=data.episode_order,
            episode_time=data.episode_time,
            watched_time=data.watched_time,
            translate_type=data.translate_type,
            episode_name=data.episode_name,
            before_watch=data.before_watch,
            after_watch=data.after_watch,
            site=data.site,
            db=db)
    except EpisodeAlreadyExists as e:
        raise HTTPException(status_code=409, detail=e.__str__())
    return episode.to_json()


@app.post("/season/create")
async def create_season_endpoint(data: SeasonCreate, db: Session = Depends(get_db)):
    try:
        season = create_season(
            season_name=data.season_name,
            title_name=data.title_name,
            episodes_count=data.episodes_count,
            watch_motivation=data.watch_motivation,
            summary=data.summary,
            season_order=data.season_order,
            db=db)
    except SeasonAlreadyExists as e:
        raise HTTPException(status_code=409, detail=e.__str__())
    return season.to_json()


@app.get("/like/title")
async def most_like_title_endpoint(search: str, db: Session = Depends(get_db)):
    title = get_most_like_title(db, search)

    return title.to_json()


@app.get("/like/season")
async def most_like_season_endpoint(search: str, db: Session = Depends(get_db)):
    season = get_most_like_season(db, search)

    return season.to_json()


@app.get("/like/title/season")
async def most_like_season_in_title_endpoint(titleName: str, search: str, db: Session = Depends(get_db)):
    season = get_most_like_season_in_title(db, titleName, search)

    return season.to_json()


@app.get("/recent/episode")
async def get_recent_watched_episode_endpoint(db: Session = Depends(get_db)):
    episode = get_recent_watched_episode(db)

    return episode.to_jsonf()


@app.get("/season/watched/episodes")
async def get_season_watched_episodes_endpoint(seasonName: str, db: Session = Depends(get_db)):
    try:
        episodes = get_season_watched_episodes(db, seasonName)
    except SeasonDontExists as e:
        raise HTTPException(status_code=404, detail=e.__str__())
    return [episode.to_json() for episode in episodes]


@app.get("/episodes/bysite")
async def get_episodes_by_site_endpoint(site: str, db: Session = Depends(get_db)):
    episodes = get_episodes_by_site(db, site)
    return [episode.to_json() for episode in episodes]

