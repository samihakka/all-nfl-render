import dash
from dash import dcc, html, Input, Output, callback, State, dash_table, MATCH
import pandas as pd
from helpers.mongo_support import MongoConnect
import dash_bootstrap_components as dbc

mongo = MongoConnect()

dash.register_page(__name__, path='/league-leaders')

document = mongo.load("getting_there")

array_of_dicts = list(document['team_stats'].values())

df2 = pd.DataFrame(array_of_dicts)


df2 = df2.sort_values(by='points for', ascending=False)
best_5_pf_df = df2.head(5)
best_5_pf_df_card = best_5_pf_df[['name', 'points for', 'logo']]

df2 = df2.sort_values(by='points for', ascending=True)
worst_5_pf_df = df2.head(5)
worst_5_pf_df_card = worst_5_pf_df[['name', 'points for', 'logo']]

df2 = df2.sort_values(by='points against', ascending=False)
worst_5_pa_df = df2.head(5)
worst_5_pa_df_card = worst_5_pa_df[['name', 'points against', 'logo']]

df2 = df2.sort_values(by='points against', ascending=True)
best_5_pa_df = df2.head(5)
best_5_pa_df_card = best_5_pa_df[['name', 'points against', 'logo']]

# print()
# print("!!!!!!!")



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
                        html.P(f"Points: {int(row[point_type])}")
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
        html.H2("Leaders and Losers.", style={"textAlign": 'center'}),
        html.Br(),
        

        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(create_single_card(best_5_pf_df_card, "Best 5 Teams Points FOR", "points for"), width=6),
                        dbc.Col(create_single_card(worst_5_pf_df_card, "Worst 5 Teams Points FOR", "points for"), width=6),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(create_single_card(best_5_pa_df_card, "Best 5 Teams Points AGAINST", "points against"), width=6),
                        dbc.Col(create_single_card(worst_5_pa_df_card, "Worst 5 Teams Points AGAINST", "points against"), width=6),
                    ],
                    className="mb-4",
                ),
            ],
            fluid=True,
        ),


    ],
    style={
        'background-image': 'url("/assets/soccer.jpeg")',
        'backgroundSize': 'cover',
        'backgroundAttachment': 'fixed',
        'overflow': 'auto',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',  # Center horizontally
        'padding': '2rem',  # Add some padding around the content
    }
)
