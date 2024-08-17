import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

bb_meme = "assets/bb_meme.png"

text_block = {
    "textAlign": "center",
    "font-weight": "bold",
    "border": "2px solid white",  # White border with 2px thickness
    "padding": "10px",  # Add some padding inside the border
    "backgroundColor": "white",  # White background inside the border
    "color": "black",  # Black text color for contrast
    "border-radius": "5px",  # Optional: rounded corners
    "display": "block",  # Use block to take full width available
    "margin": "0 auto",  # Center the block horizontally
} 

layout = html.Div([
        html.Div(style={'height': '50px'}),
        html.H1("Welcome to the Home Page. Hope ya not a Cleveland Steamah!", style=text_block),
        html.Br(),
        html.P("Look, you seem like a nice kid. Just take it easy out there, aigh?", style=text_block),
        html.Br(),
        # html.Img(src=bb_meme, style={
        #         "display": "block",
        #         "margin-left": "auto",
        #         "margin-right": "auto",
        #         "width": "20%"  # Optional: Adjust the width of the image
        #     }),
        html.Div(style={'height': '1000px'})
    ],
    style={
        'background-image': 'url("/assets/warner.jpeg")',
        'backgroundSize': 'cover',  # To cover the whole page
        # 'height': '100vh',
        'textAlign': 'center',  # Center-align text inside the container
        'display': 'flex',  # Ensure the container uses flex layout
        'flexDirection': 'column',  # Align items in a column
        'justifyContent': 'center'# Center items vertically
    }
)

