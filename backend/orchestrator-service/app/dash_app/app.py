import pandas as pd
from dash import Dash, Input, Output, dash_table, dcc, html

from app.dash_app.charts import bar_tags, donut_mode, line_chart
from app.dash_app.data import load_events
from app.dash_app.transforms import (
    events_by_mode,
    events_by_tags,
    events_per_day,
    filter_events,
)

app = Dash(__name__)


# ========================= LAYOUT =========================
app.layout = html.Div(
    className="dash-root",
    children=[
        html.H3("Global Hackathons", className="dash-title"),
        # ---------- FILTERS ----------
        html.Div(
            className="dash-filters",
            children=[
                dcc.Dropdown(
                    id="mode-filter",
                    multi=True,
                    placeholder="Mode",
                ),
                dcc.DatePickerRange(id="date-filter"),
            ],
        ),
        # ---------- TOP FULL WIDTH LINE ----------
        html.Div(
            className="dash-grid-1",
            children=[
                dcc.Graph(id="date-chart"),
            ],
        ),
        # ---------- SECOND ROW ----------
        html.Div(
            className="dash-grid-tags",
            children=[
                html.Div(dcc.Graph(id="mode-chart"), className="donut-box"),
                html.Div(dcc.Graph(id="tag-chart"), className="tag-box"),
            ],
        ),
        # ---------- TABLE ----------
        html.Div(
            className="dash-table-wrapper",
            children=[
                dash_table.DataTable(
                    id="event-table",
                    columns=[
                        {"name": "Title", "id": "title"},
                        {"name": "Mode", "id": "mode"},
                        {"name": "Start Date", "id": "start_date"},
                        {"name": "End Date", "id": "end_date"},
                        {
                            "name": "Apply",
                            "id": "registration_url",
                            "presentation": "markdown",
                        },
                    ],
                    page_size=8,
                    style_as_list_view=True,
                    style_cell={
                        "fontSize": "13px",
                        "padding": "6px",
                        "textAlign": "left",
                        "whiteSpace": "normal",
                    },
                )
            ],
        ),
    ],
)


# ========================= INITIAL FILTER LOAD =========================
@app.callback(
    Output("mode-filter", "options"),
    Output("date-filter", "start_date"),
    Output("date-filter", "end_date"),
    Input("date-filter", "id"),
)
def init_filters(_):
    df = load_events()

    df["start_date"] = pd.to_datetime(df["start_date"])

    return (
        [{"label": m, "value": m} for m in sorted(df["mode"].dropna().unique())],
        df["start_date"].min().strftime("%Y-%m-%d"),
        df["start_date"].max().strftime("%Y-%m-%d"),
    )


# ========================= MAIN DASHBOARD UPDATE =========================
@app.callback(
    Output("mode-chart", "figure"),
    Output("tag-chart", "figure"),
    Output("date-chart", "figure"),
    Output("event-table", "data"),
    Input("mode-filter", "value"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),
)
def update_dashboard(modes, start, end):

    df = load_events()

    # ensure datetime (IMPORTANT)
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])

    # apply filters
    filtered = filter_events(df, modes, start, end)

    # ---------- TABLE ----------
    table_df = filtered.copy()

    # format dates nicely
    table_df["start_date"] = pd.to_datetime(table_df["start_date"]).dt.strftime(
        "%d %b %Y"
    )
    table_df["end_date"] = pd.to_datetime(table_df["end_date"]).dt.strftime("%d %b %Y")

    # apply link
    table_df["registration_url"] = table_df["registration_url"].apply(
        lambda x: f"[Apply]({x})"
    )

    table_data = table_df[
        ["title", "mode", "start_date", "end_date", "registration_url"]
    ].to_dict("records")

    # ---------- CHARTS ----------
    mode_fig = donut_mode(events_by_mode(filtered))
    tag_fig = bar_tags(events_by_tags(filtered))
    date_fig = line_chart(events_per_day(filtered))

    return mode_fig, tag_fig, date_fig, table_data


# ========================= RUN =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
