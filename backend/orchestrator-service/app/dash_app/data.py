# dash_app/data.py
import pandas as pd
from sqlalchemy import create_engine
from app.core.config import settings
import json

SYNC_DATABASE_URL = settings.DATABASE_URL.replace("+asyncpg", "")
engine = create_engine(SYNC_DATABASE_URL)

def load_events():
    df = pd.read_sql("SELECT * FROM events", engine)

    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])

    df["tags"] = df["tags"].apply(
        lambda x: json.loads(x) if isinstance(x, str) else x
    )

    return df
