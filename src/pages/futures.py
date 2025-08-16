import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path="/futures")

# Mock DataFrames (replace with API pulls later)
super_bowl_data = pd.DataFrame({
    "Team": ["49ers", "Chiefs", "Eagles", "Bills", "Cowboys"],
    "Odds": ["+450", "+550", "+750", "+1000", "+1200"]
})

conference_data = pd.DataFrame({
    "Conference": ["AFC", "AFC", "NFC", "NFC"],
    "Team": ["Chiefs", "Bills", "49ers", "Eagles"],
    "Odds": ["+300", "+450", "+250", "+350"]
})

division_data = pd.DataFrame({
    "Division": ["AFC East", "AFC West", "NFC East", "NFC West"],
    "Favorite": ["Bills", "Chiefs", "Eagles", "49ers"],
    "Odds": ["-120", "-150", "-140", "-200"]
})

win_totals_data = pd.DataFrame({
    "Team": ["49ers", "Chiefs", "Eagles", "Cowboys"],
    "Win Total": [11.5, 11.0, 10.5, 10.0],
    "Over Odds": ["-110", "-115", "-105", "+100"],
    "Under Odds": ["-110", "-105", "-115", "-120"]
})

# Helper function for pretty tables
def make_table(df, title):
    return dbc.Card(
        dbc.CardBody([
            html.H4(title, className="card-title text-center mb-4"),
            dash_table.DataTable(
                data=df.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df.columns],
                style_table={"overflowX": "auto"},
                style_header={
                    "backgroundColor": "#002244",
                    "color": "white",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
                style_cell={
                    "textAlign": "center",
                    "padding": "8px",
                    "fontSize": "16px",
                },
                style_data_conditional=[
                    {
                        "if": {"row_index": "odd"},
                        "backgroundColor": "#f8f9fa"
                    }
                ],
            )
        ]),
        className="shadow-sm my-4"
    )

layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("NFL Futures Betting Lines", 
                        className="text-center my-4 fw-bold",
                        style={"color": "#0d6efd"}),
                html.P(
                    "Track the latest odds for Super Bowl, Conference/Division champions, and season win totals.",
                    className="text-center text-muted mb-5"
                ),
            ]
        ),

        make_table(super_bowl_data, "🏆 Super Bowl Odds"),
        make_table(conference_data, "🏈 Conference Champions"),
        make_table(division_data, "📍 Division Champions"),
        make_table(win_totals_data, "📊 Season Win Totals"),
    ],
    fluid=True,
    className="px-4"
)