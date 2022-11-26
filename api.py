from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database.sessions import get_db
from mal.client import MALClient
from requests_types import RecordCreate, MALProxy
from schemas.records.commands import create_record, create_record_from_source
import requests

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


@app.post("/record/create")
async def create_record_endpoint(data: RecordCreate, db: Session = Depends(get_db)):
    record = create_record_from_source(
        source=data.source,
        source_type=data.source_type,
        source_id=data.source_id,
        episode_order=data.episode_order,
        watch_datetime=data.watch_datetime,
        watched_from=data.watched_from,
        watched_time=data.watched_time,
        translate_type=data.translate_type,
        comment=data.comment,
        site=data.site,
        db=db
    )
    # dump_episodes(db)  # TODO: Dumping every time... It's bad realisation! Do dumps another way!

    return record.to_json()


@app.get('/mal')
async def mal_proxy_endpoint(endpoint: str):
    client = MALClient()
    return client._client_request('get', endpoint).json()
