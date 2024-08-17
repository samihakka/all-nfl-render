import dash
from dash import dcc, html, Input, Output, callback, State, dash_table, MATCH
import pandas as pd
from helpers.mongo_support import MongoConnect
import dash_bootstrap_components as dbc

mongo = MongoConnect()

text_block = {
    "textAlign": "center",
    "font-weight": "bold",
    "border": "2px solid white",  # White border with 2px thickness
    "padding": "10px",  # Add some padding inside the border
    "backgroundColor": "white",  # White background inside the border
    "color": "black",  # Black text color for contrast
    "border-radius": "5px",  # Optional: rounded corners
    "display": "inline-block",  # Ensures the block size fits the content
    "margin-left": "15%",  # Set left margin to 15%
    "margin-right": "5%",  # Set right margin to 5%
}

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
                dbc.CardImg(src=item["logo"], top=True, style={'height': '200px', 'width': '70%', "margin": "auto"}),
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
    style={"marginLeft": "15%", "marginRight": "5%"}
)

nfc_east_cards = dbc.CardGroup(
    nfc_east_cards_arr,
    style={"marginLeft": "15%", "marginRight": "5%"}
)

nfc_south_cards = dbc.CardGroup(
    nfc_south_cards_arr,
    style={"marginLeft": "15%", "marginRight": "5%"}
)

nfc_west_cards = dbc.CardGroup(
    nfc_west_cards_arr,
    style={"marginLeft": "15%", "marginRight": "5%"}
)

afc_north_cards = dbc.CardGroup(
    afc_north_cards_arr,
    style={"marginLeft": "15%", "marginRight": "5%"}
)

afc_east_cards = dbc.CardGroup(
    afc_east_cards_arr,
    style={"marginLeft": "15%", "marginRight": "5%"}
)

afc_south_cards = dbc.CardGroup(
    afc_south_cards_arr,
    style={"marginLeft": "15%", "marginRight": "5%"}
)

afc_west_cards = dbc.CardGroup(
    afc_west_cards_arr,
    style={"marginLeft": "15%", "marginRight": "5%"}
)

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


button_ids = [
    'nfc-west-button', 'nfc-north-button', 'nfc-east-button', 'nfc-south-button',
    'afc-west-button', 'afc-north-button', 'afc-east-button', 'afc-south-button'
]

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "150px",
    "left": "5px",
    "bottom": "75px",
    "width": "15%",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "border-radius": "15px",  # Adjust the radius as needed
    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",  # Optional: Adds a subtle shadow for better visual effect
    'min-height': '700px',
    'max-height': '700px',
    'min-width': '200px'
}

sidebar = html.Div(
    [
        html.H4("Select a Division", className="display-5", style = {'textAlign': 'center'}),
        html.Hr(),
        html.Img(src='assets/nfc.jpg', style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '100px'}),
        html.Div(style={'height': '15px'}),
        html.Div([
            html.A(html.Button('NFC West', id='nfc-west-button', n_clicks=0, className='btn btn-outline-primary', style={'width': '100%'}), href='#nfc-west-ts'),
            html.A(html.Button('NFC North', id='nfc-north-button', n_clicks=0, className='btn btn-outline-primary', style={'width': '100%'}), href='#nfc-north-ts'),
        ], style={
            'display': 'flex',
            'flex-direction': 'row',
            'align-items': 'center',
            'gap': '10px',         
            'width': '100%',          
            'max-width': '200px',       
            'margin': 'auto'            
        }),
        html.Div(style={'height': '5px'}),
        html.Div([
            html.A(html.Button('NFC East', id='nfc-east-button', n_clicks=0, className='btn btn-outline-primary', style={'width': '100%'}), href='#nfc-east-ts'),
            html.A(html.Button('NFC South', id='nfc-south-button', n_clicks=0, className='btn btn-outline-primary', style={'width': '100%'}), href='#nfc-south-ts'),
        ], style={
            'display': 'flex',
            'flex-direction': 'row',
            'align-items': 'center',
            'gap': '10px',         
            'width': '100%',          
            'max-width': '200px',       
            'margin': 'auto'            
        }),
        html.Div(style={'height': '50px'}),
        html.Img(src='assets/afc.jpg', style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '100px'}),
        html.Div(style={'height': '15px'}),
        html.Div([
            html.A(html.Button('AFC West', id='afc-west-button', n_clicks=0, className='btn btn-outline-primary', style={'width': '100%'}), href='#afc-west-ts'),
            html.A(html.Button('AFC North', id='afc-north-button', n_clicks=0, className='btn btn-outline-primary', style={'width': '100%'}), href='#afc-north-ts'),
        ], style={
            'display': 'flex',
            'flex-direction': 'row',
            'align-items': 'center',
            'gap': '10px',         
            'width': '100%',          
            'max-width': '200px',       
            'margin': 'auto'            
        }),
        html.Div(style={'height': '5px'}),
        html.Div([
            html.A(html.Button('AFC East', id='afc-east-button', n_clicks=0, className='btn btn-outline-primary', style={'width': '100%'}), href='#afc-east-ts'),
            html.A(html.Button('AFC South', id='afc-south-button', n_clicks=0, className='btn btn-outline-primary', style={'width': '100%'}), href='#afc-south-ts'),
        ], style={
            'display': 'flex',
            'flex-direction': 'row',
            'align-items': 'center',
            'gap': '10px',         
            'width': '100%',          
            'max-width': '200px',       
            'margin': 'auto'            
        }),
    ],
    style=SIDEBAR_STYLE,
)

layout = html.Div(
    [
        sidebar,
        html.Br(),
        # navbar,
        html.H2("NFC West", style=text_block, id="nfc-west-ts"),
        nfc_west_cards,
        html.Br(),
        html.H2("NFC North", style=text_block, id="nfc-north-ts"),
        nfc_north_cards,
        html.Br(),
        html.H2("NFC East", style=text_block, id="nfc-east-ts"),
        nfc_east_cards,
        html.Br(),
        html.H2("NFC South", style=text_block, id="nfc-south-ts"),
        nfc_south_cards,
        html.Br(),
        html.H2("AFC West", style=text_block, id="afc-west-ts"),
        afc_west_cards,
        html.Br(),
        html.H2("AFC North", style=text_block, id="afc-north-ts"),
        afc_north_cards,
        html.Br(),
        html.H2("AFC East", style=text_block, id="afc-east-ts"),
        afc_east_cards,
        html.Br(),
        html.H2("AFC South", style=text_block, id="afc-south-ts"),
        afc_south_cards,
        html.Div(style={'height': '50px'})
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

@callback(
    [Output(button_id, 'className') for button_id in button_ids],
    [Input(button_id, 'n_clicks') for button_id in button_ids]
)
def update_button_styles(*n_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ['btn btn-outline-primary' for _ in button_ids]
    
    clicked_button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    updated_classes = []
    for button_id in button_ids:
        if button_id == clicked_button_id:
            updated_classes.append('btn btn-primary')
        else:
            updated_classes.append('btn btn-outline-primary')
    
    return updated_classes