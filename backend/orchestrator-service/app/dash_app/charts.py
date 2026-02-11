import plotly.express as px

def donut_mode(df):
    fig = px.pie(
        df,
        names="mode",
        values="count",
        hole=0.5,
    )

    fig.update_layout(
        title="Event Mode",
        title_font=dict(size=14),
        margin=dict(t=35, b=20),
        font=dict(size=12),
    )

    return fig


def bar_event_type(df):
    fig = px.bar(
        df,
        x="event_type",
        y="count",
    )
    fig.update_layout(
        title="Events Types",
        title_font=dict(size=14),
        margin=dict(t=30, b=20),
        font=dict(size=12),
    )
    return fig


def bar_platform(df):
    fig = px.bar(
        df,
        x="count",
        y="platform",
        orientation="h",
    )

    fig.update_layout(
        title="Platforms Hosting Events",
        title_font=dict(size=14),
        margin=dict(t=35, b=20),
        font=dict(size=12),
        yaxis=dict(categoryorder="total ascending"),
    )

    return fig


def line_chart(df):
    fig = px.line(
        df,
        x="start_date",
        y="count",
        markers=True,
    )

    fig.update_traces(
        line=dict(width=2),
        marker=dict(size=6),
    )

    fig.update_layout(
        title="Events Over Time",
        title_font=dict(size=14),
        margin=dict(t=35, b=20),
        font=dict(size=12),
        xaxis=dict(
            tickformat="%d %b",  
            tickangle=-45
        ),
    )

    return fig
