from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import SUPERSET_METADATA_URL

engine = create_engine(SUPERSET_METADATA_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
