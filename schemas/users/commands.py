from datetime import datetime
from typing import Tuple

from sqlalchemy import or_
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

from database.tables import User
from superset.users import create_user_in_superset, get_user_from_superset
from schemas.users.exceptions import UserAlreadyExists


def register_new_user(db: Session, username: str, email: str, password: str, first_name: str or None,
                      last_name: str or None):
    if db.query(User).filter(or_(User.username==username, User.email==email)).first() or get_user_from_superset(username):
        raise UserAlreadyExists(f'User with username {username} or email {email} already exists')
    gen_first_name, gen_last_name = generate_user_name()
    first_name, last_name = gen_first_name if not first_name else first_name, \
                            gen_last_name if not last_name else last_name

    hashed_password = generate_password_hash(password)
    now = datetime.now()

    user_db = create_user(db=db, username=username, email=email, hashed_password=hashed_password, first_name=first_name,
                          last_name=last_name, created_on=now)

    create_user_in_superset(username=username, email=email, hashed_password=hashed_password, active=True,
                            created_on=now.strftime('%Y-%m-%d %H:%M:%S'), first_name=first_name, last_name=last_name)


def is_password_right(user: User, password: str):
    return check_password_hash(user.password, password)


def generate_user_name() -> Tuple[str, str]:
    # TODO: Make generations like in google sheets
    """
    Returning first and last name for no passed
    :return:
    """

    return 'No first name', 'No last name'


def create_user(db: Session, username: str, email: str, hashed_password: str, first_name: str, last_name: str,
                created_on: datetime):
    _user = User(
        username=username,
        email=email,
        password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        created_on=created_on,
    )
    db.add(_user)
    db.commit()
    return _user


def check_password(username: str, password: str):  # TODO: Add checking it from db user and use in api.py for loggining
    pass
