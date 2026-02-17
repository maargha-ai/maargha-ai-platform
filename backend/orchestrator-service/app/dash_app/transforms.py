import pandas as pd

def filter_events(df, modes, start, end):
    filtered = df.copy()

    if modes:
        filtered = filtered[filtered["mode"].isin(modes)]

    if start and end:
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)

        filtered = filtered[
            (filtered["start_date"] >= start) &
            (filtered["start_date"] <= end)
        ]

    return filtered


def events_per_day(df):
    return (
        df.groupby("start_date")
        .size()
        .reset_index(name="count")
        .sort_values("start_date")
    )


def events_by_mode(df):
    return (
        df.groupby("mode")
        .size()
        .reset_index(name="count")
    )


def events_by_tags(df):
    if "tags" not in df.columns:
        return pd.DataFrame(columns=["tag", "count"])

    exploded = df.explode("tags")

    exploded["tag"] = exploded["tags"].apply(
        lambda x: x.get("name") if isinstance(x, dict) else None
    )

    exploded = exploded.dropna(subset=["tag"])

    return exploded.groupby("tag").size().reset_index(name="count")