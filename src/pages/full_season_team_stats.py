import dash
from dash import dcc, html, Input, Output, callback, State, dash_table, MATCH
import pandas as pd
from helpers.mongo_support import MongoConnect
import dash_bootstrap_components as dbc

mongo = MongoConnect()

# Initialize the Dash app
dash.register_page(__name__, path='/full-season-team-stats')
sandbox = ["display", "logo", "logo_html"]

document = mongo.load("getting_there")
# print(list(document['team_stats'].values()))
array_of_dicts = list(document['team_stats'].values())
df2 = pd.DataFrame(array_of_dicts)
# df2['display'] = df2['logo'].apply(lambda x: f'![Logo]({x})')
# df2['display'] = df2['logo'].apply(lambda x: f'![Logo]({x}){{: style="height:50px; width:50px;"}}')
df2 = df2.drop(columns=['game_log'])
df2 = df2.drop(columns=['logo'])


all_teams = document['team_stats']
team_id_dic = {}

for team in all_teams:
    team_id_dic[document["team_stats"][team]["name"]] = team

print("team_id dic from full_season_team_stats", team_id_dic)

df_new = array_of_dicts[28]
# print(df_new["game_log"])

niners_games_df = pd.DataFrame(df_new["game_log"])


ari_logo_path = 'assets/ari.png'
sf_logo_path = "https://a.espncdn.com/i/teamlogos/nfl/500/sf.png"
lar_logo_path = "https://a.espncdn.com/i/teamlogos/nfl/500/lar.png"
sea_logo_path = "https://a.espncdn.com/i/teamlogos/nfl/500/sea.png"

# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Page 1", href="#")),
#         dbc.DropdownMenu(
#             children=[
#                 dbc.DropdownMenuItem("More pages", header=True),
#                 dbc.DropdownMenuItem("Page 2", href="#"),
#                 dbc.DropdownMenuItem("Page 3", href="#"),
#             ],
#             nav=True,
#             in_navbar=True,
#             label="More",
#         ),
#     ],
#     brand="All NFL Dashboard",
#     brand_href="#",
#     color="primary",
#     dark=True,
# )

nfc_north_cards_arr = []
nfc_south_cards_arr = []
nfc_east_cards_arr = []
nfc_west_cards_arr = []

nfc_west = ["SF", "LAR", "ARI", "SEA"]
nfc_north = ["GB", "MIN", "DET", "CHI"]
nfc_south = ["ATL", "TB", "CAR", "NO"]
nfc_east = ["PHI", "DAL", "NYG", "WSH"]

afc_north_cards_arr = []
afc_south_cards_arr = []
afc_east_cards_arr = []
afc_west_cards_arr = []

afc_west = ["KC", "LAC", "DEN", "LV"]
afc_north = ["BAL", "CIN", "CLE", "PIT"]
afc_south = ["HOU", "IND", "JAX", "TEN"]
afc_east = ["BUF", "MIA", "NE", "NYJ"]



for i, item in enumerate(array_of_dicts):

    curr_card = (dbc.Card(
            [
                dbc.CardImg(src=item["logo"], top=True, style={'height': '200px', 'width': '200px', "margin": "auto"}),
                dbc.CardBody(
                    [
                        html.H4(item["name"], className="card-title", style={"textAlign": "center"}),
                        html.P(
                            f"Record: {item['wins']}-{item['losses']}",
                            className="card-text",
                            style={"textAlign": "center"}
                        ),
                        html.Div(
                            [
                                dbc.Button("View Game Schedule", id={"type": "open-centered", "index": item["name"]}),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(dbc.ModalTitle(item["name"] + " schedule"), close_button=True),
                                        dbc.ModalBody(dash_table.DataTable(
                                            data=item["game_log"],
                                            columns=[{"name": i, "id": i} for i in item["game_log"][0].keys()],
                                            style_table={'overflowX': 'auto'},
                                            style_cell={'textAlign': 'left'},
                                            style_data_conditional=[
                                                {
                                                    'if': {
                                                        'column_id': 'result',
                                                        'filter_query': '{result} = "L"'
                                                    },
                                                    'color': 'red'
                                                },
                                                {
                                                    'if': {
                                                        'column_id': 'result',
                                                        'filter_query': '{result} = "W"'
                                                    },
                                                    'color': 'green'
                                                }
                                            ]
                                        )),
                                        dbc.ModalFooter(
                                            dbc.Button(
                                                "Close",
                                                id={"type": "close-centered", "index": item["name"]},
                                                className="ms-auto",
                                                n_clicks=0,
                                            )
                                        ),
                                    ],
                                    id={"type": "modal-centered", "index": item["name"]},
                                    size="xl",
                                    centered=True,
                                    is_open=False,
                                ),
                            ],
                            style={"margin": "auto", "textAlign": "center"}
                        )
                    ]
                ),
            ],
            style={"width": "18rem"},
        ))
    if item["name"] in nfc_north:
        nfc_north_cards_arr.append(curr_card)
    elif item["name"] in nfc_south:
        nfc_south_cards_arr.append(curr_card)
    elif item["name"] in nfc_east:
        nfc_east_cards_arr.append(curr_card)
    elif item["name"] in nfc_west:
        nfc_west_cards_arr.append(curr_card)
    elif item["name"] in afc_south:
        afc_south_cards_arr.append(curr_card)
    elif item["name"] in afc_east:
        afc_east_cards_arr.append(curr_card)
    elif item["name"] in afc_west:
        afc_west_cards_arr.append(curr_card)
    elif item["name"] in afc_north:
        afc_north_cards_arr.append(curr_card)

nfc_north_cards = dbc.CardGroup(
    nfc_north_cards_arr,
    style={"marginLeft": "5%", "marginRight": "5%"}
)

nfc_east_cards = dbc.CardGroup(
    nfc_east_cards_arr,
    style={"marginLeft": "5%", "marginRight": "5%"}
)

nfc_south_cards = dbc.CardGroup(
    nfc_south_cards_arr,
    style={"marginLeft": "5%", "marginRight": "5%"}
)

nfc_west_cards = dbc.CardGroup(
    nfc_west_cards_arr,
    style={"marginLeft": "5%", "marginRight": "5%"}
)

afc_north_cards = dbc.CardGroup(
    afc_north_cards_arr,
    style={"marginLeft": "5%", "marginRight": "5%"}
)

afc_east_cards = dbc.CardGroup(
    afc_east_cards_arr,
    style={"marginLeft": "5%", "marginRight": "5%"}
)

afc_south_cards = dbc.CardGroup(
    afc_south_cards_arr,
    style={"marginLeft": "5%", "marginRight": "5%"}
)

afc_west_cards = dbc.CardGroup(
    afc_west_cards_arr,
    style={"marginLeft": "5%", "marginRight": "5%"}
)

# table = dash_table.DataTable(
#     id="records-table",
#     style_table={ 
#         'overflowX': 'auto',
#         'overflowY': 'auto',
#         'width': '50%',
#         'maxHeight': '70rem',
#         'margin': 'auto',
#     },
#     style_cell={
#         'whiteSpace': 'normal',
#         'maxHeight': '20px',
#         'margin': 'auto',
#         'minWidth': '5vw', 'maxWidth': '20vw',
#         'overflow': 'hidden', 'textAlign': 'center'
#     },
#     style_data={
#         'whiteSpace': 'normal',
#         'height': 'auto',
#         'border': 'none'
#     },
#     columns=[
#         {"name": i, "id": i, "presentation": "markdown"} if i in sandbox else {"name": i, "id": i}
#         for i in niners_games_df.columns
#     ], 
#     data=niners_games_df.to_dict('records'),
# )

@callback(
    Output({"type": "modal-centered", "index": MATCH}, "is_open"),
    Input({"type": "open-centered", "index": MATCH}, "n_clicks"),
    Input({"type": "close-centered", "index": MATCH}, "n_clicks"),
    State({"type": "modal-centered", "index": MATCH}, "is_open"),
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

layout = html.Div(
    [
        # navbar,
        html.H2("NFC West", style={"textAlign": "center", "font-weight": "bold"}),
        nfc_west_cards,
        html.Br(),
        html.H2("NFC North", style={"textAlign": "center", "font-weight": "bold"}),
        nfc_north_cards,
        html.Br(),
        html.H2("NFC East", style={"textAlign": "center", "font-weight": "bold"}),
        nfc_east_cards,
        html.Br(),
        html.H2("NFC South", style={"textAlign": "center", "font-weight": "bold"}),
        nfc_south_cards,
        html.Br(),
        html.H2("AFC West", style={"textAlign": "center", "font-weight": "bold"}),
        afc_west_cards,
        html.Br(),
        html.H2("AFC North", style={"textAlign": "center", "font-weight": "bold"}),
        afc_north_cards,
        html.Br(),
        html.H2("AFC East", style={"textAlign": "center", "font-weight": "bold"}),
        afc_east_cards,
        html.Br(),
        html.H2("AFC South", style={"textAlign": "center", "font-weight": "bold"}),
        afc_south_cards,
    ],
)

