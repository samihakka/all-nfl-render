# import dash
# from dash import dcc, html, Input, Output, callback, State, dash_table, MATCH
# import pandas as pd
# from helpers.mongo_support import MongoConnect
# import plotly.graph_objects as go
# import dash_bootstrap_components as dbc
# from dash.exceptions import PreventUpdate

# mongo = MongoConnect()

# from helpers.helper_betting import BettingHelper
# helper = BettingHelper()

# # Initialize the Dash app
# # dash.register_page(__name__, path='/betting')


# # load correct df
# document = mongo.load("getting_there")

# all_teams = document["team_stats"]

# team_id_dic = {}
# for team in all_teams:
#     team_id_dic[document["team_stats"][team]["name"]] = team


# # print("num teams: ", len(all_teams))
# # print(team_id_dic)

# ou_dropdown_options = [{"label": key, "value": key} for key in team_id_dic.keys()]

# ou_dropdown = html.Div(
#         dcc.Dropdown(
#             id="ou-dropdown",
#             options=ou_dropdown_options,
#             placeholder="Select a team",
#             value=None,
#             style={"width": "40%"}  # Adjust width as needed
#         )
# )

# spread_dropdown = html.Div(
#         dcc.Dropdown(
#             id="spread-dropdown",
#             options=ou_dropdown_options,
#             placeholder="Select a team",
#             value="ARI",
#             style={"width": "40%"}  # Adjust width as needed
#         )
# )



# layout = html.Div(
#     [
#         html.H1("All things betting"),
#         ou_dropdown,
#         html.Div(id='bar-graph-container', style={'margin': '0 7%'}),
#         spread_dropdown,
#         html.Div(id='bar-graph-container-spread', style={'margin': '0 7%'})
#     ],
# )


# ########
# ##  BEGINNING OF CALLBACK FUNCTIONS
# ########
# @callback(
#     Output("bar-graph-container", "children"),
#     Output("bar-graph-container", "style"),
#     Input("ou-dropdown", "value")
# )
# def update_graph(selected_team):
#     if selected_team is None:
#             raise PreventUpdate
#     id = team_id_dic[selected_team]
#     print("selected team: ", id)
#     team_data = document["team_stats"][id]
#     logs = team_data["game_log"]

#     layout = helper.build_bar_graph(selected_team, team_id_dic, logs, team_data["logo"])

#     return layout, {
#         "display": "flex",  # Use flexbox to align items in a row
#         "align-items": "center",  # Center items vertically within the container
#         "width": "90%"  # Ensure container takes full width
#     }



# ########
# ##  BEGINNING OF CALLBACK FUNCTIONS
# ########
# @callback(
#     Output("bar-graph-container-spread", "children"),
#     Output("bar-graph-container-spread", "style"),
#     Input("spread-dropdown", "value")
# )
# def update_graph_spread(selected_team):
#     if selected_team is None:
#         raise PreventUpdate
#     id = team_id_dic[selected_team]
#     print("selected team: ", id)
#     team_data = document["team_stats"][id]
#     logs = team_data["game_log"]

#     layout = helper.build_bar_graph_spread(selected_team, team_id_dic, logs, team_data["logo"])

#     return layout, {
#         "display": "flex",  # Use flexbox to align items in a row
#         "align-items": "center",  # Center items vertically within the container
#         "width": "90%"  # Ensure container takes full width
#     }
