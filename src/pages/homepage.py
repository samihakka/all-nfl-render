import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

# bb_meme = "assets/bb_meme.png"

layout = html.Div([
    html.H1("Welcome to the Home Page. Hope ya not a Cleveland Steamah!", style={"textAlign": "center"}),
    html.P("Look, you seem like a nice kid. Just take it easy out there, aigh?", style={"textAlign": "center"}),
    # html.Img(src=bb_meme, style={
    #         "display": "block",
    #         "margin-left": "auto",
    #         "margin-right": "auto",
    #         "width": "20%"  # Optional: Adjust the width of the image
    #     })
])