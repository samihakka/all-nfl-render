import dash
from dash import dcc, html, Input, Output, callback, State, dash_table, MATCH
import pandas as pd
from helpers.mongo_support import MongoConnect
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

mongo = MongoConnect()

from helpers.helper_betting import BettingHelper
helper = BettingHelper()

# Initialize the Dash app
dash.register_page(__name__, path='/betting-advanced')


######################### mE!!!
# load correct df
document = mongo.load("getting_there")

all_teams = document["team_stats"]

team_id_dic = {}
for team in all_teams:
    team_id_dic[document["team_stats"][team]["name"]] = team


team_spreads = {}
for team in all_teams:
    # print(all_teams[team]["avg_spread"])
    team_spreads[all_teams[team]["name"]] = all_teams[team]["avg_spread"]
print(team_spreads)
team_spreads = dict(sorted(team_spreads.items(), key=lambda item: item[1]))
print(team_spreads)

# print("num teams: ", len(all_teams))
# print(team_id_dic)

ou_dropdown_options = [{"label": key, "value": key} for key in team_id_dic.keys()]
######################### mE!!!

colors = {
    'text': '#000000',
    'primary': '#3465DA'
}

spread_button = html.Div(
    dbc.Button("Spread", active=True, color='primary', outline=True, id="Spread", className="me-1", style={"width": "10rem", "height": "3rem", "border-radius": "50rem"}),
    style={"display": "flex", "justify-content": "cneter", "align-items": "center", "padding": "0.5rem"},
)

ou_button = html.Div(
    dbc.Button("Over/Under", color='primary', outline=True, id="Over/Under", className="me-1", style={"width": "10rem", "height": "3rem", "border-radius": "50rem"}),
    style={"display": "flex", "justify-content": "cneter", "align-items": "center", "padding": "0.5rem"},
)

side_nav = dbc.Card(
    className="m-5 p-2 rounded-3",
    children=[
        dbc.CardHeader(html.H4("Flavors"), className="text-center"),
        dbc.CardBody(
            children=[
                spread_button,
                ou_button
            ],
            className="p=0 pt-3"
        )
    ]
)

def create_spread():
    layout = helper.load_spread_page(team_id_dic, team_spreads)
    return layout

def create_overunder():
    return helper.load_ou_page(team_id_dic)

children = create_spread()

layout = html.Div(
    # style={"display": "flex", "height": "100vh"},
    children = [

        html.Div(
            side_nav,
            style={"flex": "0 0 12%"}
        ),
        html.Div(
            id="data-container",
            children=children,
            style={"flex": "1", "display": "flex", "flex-wrap": "wrap", "justify-content": "center"}
        ),
        html.Div(style={'height': '1000px'})


    ],
    style={
        'background-image': 'url("/assets/real_chino.jpeg")',
        'backgroundSize': 'cover',
        'backgroundAttachment': 'fixed',
        'overflow': 'auto',
        'display': 'flex',
        # 'alignItems': 'center',  # Center horizontally
        'padding': '2rem',  # Add some padding around the content
        "height": "100%"
    }
    

)


@callback(
        Output("Spread", "active"),
        Output("Over/Under", "active"),
        Input("Spread", "n_clicks"),
        Input("Over/Under", "n_clicks"),
        prevent_initial_call = True
)
def update_active_button(spread_button, ou_button):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = "No button clicked yet."
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    spread_active = ou_active = False
    if spread_button is None and ou_button is None:
        spread_active = True
    else:
        if button_id == "Spread":
            spread_active = True 
        elif button_id == "Over/Under":
            print("OU ACTIVE TRUE")
            ou_active = True
    return spread_active, ou_active

@callback(
    Output("data-container", "children"),
    Input("Spread", "n_clicks"),
    Input("Over/Under", "n_clicks"),
    prevent_initial_call = True
)
def display_button(*args):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = "No button clicked yet."
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "Spread":
        children = create_spread()
    elif button_id == "Over/Under":
        children = create_overunder()
    else:
        children = f"Hello from {button_id}"
    return children






# / / / / / / / / / / / / / / / /  CALLBACKS / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /

########
##  BEGINNING OF CALLBACK FUNCTIONS
########
@callback(
    Output("bar-graph-container", "children"),
    Output("bar-graph-container", "style"),
    Input("ou-dropdown", "value")
)
def update_graph(selected_team):
    if selected_team is None:
            raise PreventUpdate
    id = team_id_dic[selected_team]
    print("selected team: ", id)
    team_data = document["team_stats"][id]
    logs = team_data["game_log"]

    layout = helper.build_bar_graph(selected_team, team_id_dic, logs, team_data["logo"])

    return layout, {
        "display": "flex",  # Use flexbox to align items in a row
        "align-items": "center",  # Center items vertically within the container
        "width": "90%"  # Ensure container takes full width
    }



@callback(
    Output("bar-graph-container-spread", "children"),
    Output("bar-graph-container-spread", "style"),
    Input("spread-dropdown", "value")
)
def update_graph_spread(selected_team):
    if selected_team is None:
        raise PreventUpdate
    id = team_id_dic[selected_team]
    print("selected team: ", id)
    team_data = document["team_stats"][id]
    logs = team_data["game_log"]

    layout = helper.build_bar_graph_spread(selected_team, team_id_dic, logs, team_data["logo"])
    print("yea....")
    return layout, {
        "display": "flex",  # Use flexbox to align items in a row
        "align-items": "center",  # Center items vertically within the container
        "width": "90%"  # Ensure container takes full width
    }