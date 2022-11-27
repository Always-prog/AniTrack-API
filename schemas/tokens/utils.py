from os import urandom

from sqlalchemy.orm import Session

from database.tables import User, Token


def generate_token() -> str:
    return urandom(32).hex()


def create_new_user_token(db: Session, user: User):
    token = generate_token()
    _token = Token(
        user_id=user.id,
        token=token
    )
    db.add(_token)
    db.commit()
    return token
