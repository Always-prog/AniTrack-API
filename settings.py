import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
DUMP_SCRIPT_PATH = os.getenv('DUMP_SCRIPT_PATH')
EPISODES_TXT_FILE_PATH = os.getenv('EPISODES_TXT_FILE_PATH')
