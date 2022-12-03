from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.sessions import get_db
from database.tables import User, Token
from mal.client import MALClient
from requests_types import RecordCreate, Register
from schemas.records.commands import create_record_from_source
from schemas.tokens.utils import create_new_user_token
from schemas.users.commands import register_new_user, check_user_password
from schemas.users.exceptions import UserAlreadyExists

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/register")
async def register(data: Register, db: Session = Depends(get_db)):
    try:
        register_new_user(db=db, username=data.username, email=data.email, password=data.password,
                          first_name=data.first_name, last_name=data.last_name)
    except UserAlreadyExists as e:
        raise HTTPException(status_code=409, detail=e.__str__())


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if check_user_password(user, form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_new_user_token(db, user)

    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_db = db.query(Token).filter_by(token=token).first()

    if not token_db:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = token_db.user

    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user


@app.get("/me")
async def get_my_user(user: User = Depends(get_current_user)):
    return user.to_json()


@app.post("/record/create")
async def create_record_endpoint(data: RecordCreate, user: User = Depends(get_current_user),
                                 db: Session = Depends(get_db)):
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
        db=db,
        user=user
    )
    # dump_episodes(db)  # TODO: Dumping every time... It's bad realisation! Do dumps another way!

    return record.to_json()


@app.get('/mal')
async def mal_proxy_endpoint(endpoint: str):
    client = MALClient()
    return client._client_request('get', endpoint).json()
