from pydantic import BaseModel
from typing import Union, Literal


class RecordCreate(BaseModel):
    source: Literal['mal']
    source_type: Literal['season']
    source_id: int
    watch_datetime: str
    episode_order: int
    watched_from: int or float
    watched_time: int or float
    translate_type: str
    comment: Union[str, None]
    site: str


class Register(BaseModel):
    username: str
    email: str
    password: str
    first_name: Union[str, None]
    last_name: Union[str, None]
    

class MALProxy(BaseModel):
    endpoint: str
    params: dict
