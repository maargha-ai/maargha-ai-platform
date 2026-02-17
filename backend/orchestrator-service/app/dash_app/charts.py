import plotly.express as px

THEME = dict(
    plot_bgcolor="#E8EDFC",
    paper_bgcolor="#FDFDFD",
    font_color="#000000"
)

def donut_mode(df):
    if df.empty:
        return px.scatter(title="No data")

    fig = px.pie(
        df,
        names="mode",
        values="count",
        hole=0.55,
    )

    fig.update_traces(
        textposition="inside",
        insidetextorientation="radial",
        sort=False,
        direction="clockwise",
        domain=dict(x=[0, 1], y=[0, 1])   # occupy FULL graph area
    )

    fig.update_layout(
        title="Hackathon Mode",
        title_font=dict(size=14),

        # remove unused padding space
        margin=dict(l=10, r=10, t=75, b=10),

        # prevents plotly from reserving legend spacing
        legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center"),

        **THEME
    )

    return fig


def line_chart(df):
    if df.empty:
        return px.scatter(title="No data")

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
        title="Hackathons Over Time",
        title_font=dict(size=14),
        margin=dict(t=35, b=20),
        xaxis=dict(
            tickformat="%d %b",
            tickangle=-45
        ),
        **THEME
    )

    return fig


def bar_tags(df):
    fig = px.bar(
        df.sort_values("count", ascending=True),
        x="count",
        y="tag",
        orientation="h",
    )

    fig.update_layout(
        title="Popular Technologies",
        title_font=dict(size=14),
        margin=dict(t=35, b=20),
        font=dict(size=12),
        yaxis=dict(categoryorder="total ascending"),
        **THEME
    )

    return fig
