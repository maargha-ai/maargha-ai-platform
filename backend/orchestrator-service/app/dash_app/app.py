from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd

from app.dash_app.data import load_events
from app.dash_app.transforms import filter_events, group_count
from app.dash_app.charts import *

df = load_events()
df["month"] = pd.to_datetime(df["start_date"]).dt.strftime("%B")
df["day"] = pd.to_datetime(df["start_date"]).dt.day

app = Dash(__name__)

app.layout = html.Div(
    className="dash-root",
    children=[

        html.H3("Global Tech Events", className="dash-title"),

        # ---------- FILTERS ----------
        html.Div(
            className="dash-filters",
            children=[
                dcc.Dropdown(
                    id="event-type-filter",
                    options=[{"label": e, "value": e} for e in sorted(df["event_type"].unique())],
                    multi=True,
                    placeholder="Event type",
                ),
                dcc.Dropdown(
                    id="mode-filter",
                    options=[{"label": m, "value": m} for m in sorted(df["mode"].unique())],
                    multi=True,
                    placeholder="Mode",
                ),
                dcc.DatePickerRange(
                    id="date-filter",
                    start_date=df["start_date"].min(),
                    end_date=df["start_date"].max(),
                ),
            ],
        ),

        # ---------- CHARTS ROW 1 ----------
        html.Div(
            className="dash-grid-2",
            children=[
                dcc.Graph(id="mode-chart"),
                dcc.Graph(id="type-chart"),
            ],
        ),

        # ---------- CHARTS ROW 2 ----------
        html.Div(
            className="dash-grid-2",
            children=[
                dcc.Graph(id="platform-chart"),
                dcc.Graph(id="date-chart"),
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
                        {"name": "Type", "id": "event_type"},
                        {"name": "Mode", "id": "mode"},
                        {"name": "Month", "id": "month"},
                        {"name": "Day", "id": "day"},
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
                        "whiteSpace": "normal",
                        "textAlign": "left",
                    },
                    style_header={
                        "fontWeight": "600",
                    },
                )
            ],
        ),
    ],
)


# ---------------- CALLBACK ----------------
@app.callback(
    Output("mode-chart", "figure"),
    Output("type-chart", "figure"),
    Output("platform-chart", "figure"),
    Output("date-chart", "figure"),
    Output("event-table", "data"),
    Input("event-type-filter", "value"),
    Input("mode-filter", "value"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),
)
def update_dashboard(event_types, modes, start, end):
    # 1️⃣ Filter data
    filtered = filter_events(df, event_types, modes, start, end)

    # 2️⃣ Prepare table data (IMPORTANT)
    table_df = filtered.copy()

    table_df["registration_url"] = table_df["registration_url"].apply(
        lambda x: f"[Apply]({x})"
    )

    table_columns = [
        "title",
        "event_type",
        "mode",
        "month",
        "day",
        "registration_url",
    ]

    table_data = table_df[table_columns].to_dict("records")

    # 3️⃣ Return charts + table
    return (
        donut_mode(group_count(filtered, "mode")),
        bar_event_type(group_count(filtered, "event_type")),
        bar_platform(group_count(filtered, "platform")),
        line_chart(group_count(filtered, "start_date")),
        table_data,
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)