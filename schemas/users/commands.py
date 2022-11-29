from superset.users import create_user_in_superset
from datetime import datetime
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from database.tables import User


#  TODO: REGISTERING NOT TESTED. TEST IT.

def register_new_user(db: Session, username: str, email: str, password: str, first_name: str, last_name: str):
    hashed_password = generate_password_hash(password)
    now = datetime.now()

    create_user(db=db, username=username, email=email, hashed_password=password, first_name=first_name,
                last_name=last_name, created_on=now)
    create_user_in_superset(username=username, email=email, hashed_password=hashed_password, active=True,
                            created_on=now.strftime('%Y-%m-%d %H:%M:%S'), first_name=first_name, last_name=last_name)


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


def check_password(username: str, password: str):  # TODO: Add checking it from db user and use in api.py for loggining
    pass
