# dash_app/transforms.py
import pandas as pd

def events_by_type(df):
    return df.groupby("event_type").size().reset_index(name="count")

def events_by_mode(df):
    return df.groupby("mode").size().reset_index(name="count")

def events_by_platform(df):
    return df.groupby("platform").size().reset_index(name="count")

def events_per_day(df):
    return (
        df.groupby("start_date")
        .size()
        .reset_index(name="count")
    )

def filter_events(df, event_types, modes, start, end):
    filtered = df.copy()

    if event_types:
        filtered = filtered[filtered["event_type"].isin(event_types)]

    if modes:
        filtered = filtered[filtered["mode"].isin(modes)]

    if start and end:
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)

        filtered["start_date"] = pd.to_datetime(filtered["start_date"])
        filtered = filtered[
            (filtered["start_date"] >= start) &
            (filtered["start_date"] <= end)
        ]

    return filtered


def group_count(df, col):
    return df.groupby(col).size().reset_index(name="count")
