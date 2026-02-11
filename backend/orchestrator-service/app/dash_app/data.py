# dash_app/data.py
import pandas as pd
from sqlalchemy import create_engine
from app.core.config import settings

SYNC_DATABASE_URL = settings.DATABASE_URL.replace("+asyncpg", "")
engine = create_engine(SYNC_DATABASE_URL)

def load_events():
    return pd.read_sql("SELECT * FROM events", engine)