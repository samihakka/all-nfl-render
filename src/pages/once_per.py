import dash
from dash import dcc, html, Input, Output, callback, State, dash_table, MATCH
import pandas as pd
from helpers.mongo_support import MongoConnect
import dash_bootstrap_components as dbc

mongo = MongoConnect()

dash.register_page(__name__, path='/once-per')

document = mongo.load("getting_there")

array_of_dicts = list(document['team_stats'].values())

df2 = pd.DataFrame(array_of_dicts)

df2 = df2.sort_values(by='spread_units_won', ascending=False)
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print(df2)
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

def create_single_card(df, title, point_type):
    card_content = []
    for i,( _, row) in enumerate(df.iterrows()):
        card_content.append(
            dbc.Row(
                [
                    dbc.Col(html.H1(f"{i+1}.")),
                    dbc.Col(html.Img(src=row['logo'], style={"width": "100px", "height": "100px", "object-fit": "contain"}), width="auto"),
                    dbc.Col([
                        html.H5(row['name']),
                        html.P(f"Units won/lost: {int(row[point_type])}")
                    ])
                ],
                className="mb-3",  # Adds margin-bottom to each row
                align="center"
            )
        )
        card = dbc.Card([
            dbc.CardHeader(html.H4(title, className="text-center")),
            dbc.CardBody(card_content),
        ],
        style={"width": "100%", "max-width": "70%", "margin": "20px auto"},
    )
    return card
    


    

layout = html.Div(
    [
        html.Br(),
        html.H2("One unit per week.", style={"textAlign": 'center'}),
        html.Br(),
        
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(create_single_card(df2, "Ranking all teams: Units won/lost", "spread_units_won"), width=6),
                    ],
                    className="mb-4",
                ),
            ],
            fluid=True,
        ),

    ],
    style={
        'background-image': 'url("/assets/real_chino.jpeg")',
        'backgroundSize': 'cover',
        'backgroundAttachment': 'fixed',
        'overflow': 'auto',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',  # Center horizontally
        'padding': '2rem',  # Add some padding around the content
    }
)
