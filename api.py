from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database.sessions import get_db
from schemas.episodes.exceptions import EpisodeAlreadyExists
from schemas.episodes.commands import create_episode
from schemas.seasons.commands import get_seasons, create_season
from schemas.seasons.exceptions import SeasonAlreadyExists
from schemas.titles.commands import get_titles, search_titles, create_title
from schemas.titles.exceptions import TitleAlreadyExists
from requests_types import TitleSearch, TitleCreate, EpisodeCreate, SeasonCreate

app = FastAPI()


@app.get("/titles")
async def all_titles_endpoint(db: Session = Depends(get_db)):
    titles = get_titles(db)
    return [title.to_json() for title in titles]


@app.get("/search/titles")
async def search_titles_endpoint(search: TitleSearch, db: Session = Depends(get_db)):
    titles = search_titles(db, search.search)
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