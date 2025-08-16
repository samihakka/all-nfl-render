import dash
from dash import dcc, html, Input, Output, callback, State, dash_table, MATCH, ALL
import pandas as pd
from helpers.mongo_support import MongoConnect
import dash_bootstrap_components as dbc

mongo = MongoConnect()

dash.register_page(__name__, path='/schedule-game')
sandbox = ["display", "logo", "logo_html"]

document = mongo.load_with_year("schedule_predict", 2024)

TEAM_ID = "2"

all_teams = document["team_schedules"]


team_id_dic = {}
for team in all_teams:
    team_id_dic[document["team_schedules"][team]["name"]] = team

team_dropdown_options = [{"label": key, "value": key} for key in team_id_dic.keys()]

dropdown = dcc.Dropdown(
            id="ou-dropdown",
            options=team_dropdown_options,
            placeholder="Select a team",
            value="ARI",
            style={"width": "50%"}  # Adjust width as needed
        )

text_block = {
    "textAlign": "center",
    "font-weight": "bold",
    "border": "2px solid white",  # White border with 2px thickness
    "padding": "10px",  # Add some padding inside the border
    "backgroundColor": "white",  # White background inside the border
    "color": "black",  # Black text color for contrast
    "border-radius": "5px",  # Optional: rounded corners
    "display": "inline-block",  # Ensures the block size fits the content
    "margin-left": "30%",  # Set left margin to 15%
    "margin-right": "5%",  # Set right margin to 5%
}

niners = document["team_schedules"][TEAM_ID]

array = [
    document["team_schedules"]["25"],
    document["team_schedules"]["22"],
    document["team_schedules"]["26"],
    document["team_schedules"]["26"],
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

def create_single_card(blank):
    card = dbc.Card([
        dbc.CardHeader(html.H1(f"Week {blank['week']}")),
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src=document["team_schedules"][blank["opponent"]]["logo"],
                            style={"width": "100px", "height": "100px", "object-fit": "contain"}
                        ),
                        width="auto"
                    ),
                    dbc.Col(html.H1(f"{blank['homeAway']}")),
                ],
                className="mb-3",
                align="center"
            )
        ),
        dbc.CardFooter(
            dbc.RadioItems(
                options=[
                    {"label": "Win", "value": "win"},
                    {"label": "Loss", "value": "loss"}
                ],
                value=None,  # No initial selection
                id={"type": "radio-items", "index": blank['week']},
                inline=True,  # Display the radio buttons inline
                className="d-flex justify-content-center"  # Center the radio buttons
            ),
            style={"textAlign": "center"}
        )
    ],
    id={"type": "card", "index": blank['week']},  # Assign a unique ID to each card
    style={"width": "100%", "max-width": "300px", "height": "300px", "margin": "10px"}  # Set max-width to 500px
    )
    return card

game_type = html.Div(
    [
        html.Div([
            html.A(
                html.Button(
                    'By Team', 
                    id='by_team_button', 
                    n_clicks=0, 
                    className='btn btn-outline-primary', 
                    style={
                        'width': '300px',
                        'height': '60px',           # Increase button height
                        'fontSize': '20px',         # Increase font size
                        'display': 'flex',
                        'alignItems': 'center',     # Center text vertically
                        'justifyContent': 'center'  # Center text horizontally
                    }
                )
            ),
            html.A(
                html.Button(
                    'By Division', 
                    id='by_division_button', 
                    n_clicks=0, 
                    className='btn btn-outline-primary', 
                    style={
                        'width': '300px',
                        'height': '60px',           # Increase button height
                        'fontSize': '20px',         # Increase font size
                        'display': 'flex',
                        'alignItems': 'center',     # Center text vertically
                        'justifyContent': 'center'  # Center text horizontally
                    }
                )
            ),
        ], style={
            'display': 'flex',
            'justifyContent': 'center',  # Center the buttons horizontally
            'alignItems': 'center',      # Optional: Center the buttons vertically
            'gap': '20px'                # Space between the buttons
        })
    ],
    style={
        'display': 'flex',
        'justifyContent': 'center',  # Center the button container horizontally on the page
        'margin': '20px'             # Optional: Add some margin around the container
    }
)



scrollable_row = dbc.Row(
    [create_single_card(blank) for blank in niners["schedule"]],
    style={
        "display": "flex",
        "flexWrap": "nowrap",  # Prevent wrapping to keep cards in a single row
        "overflowX": "auto",  # Enable horizontal scrolling
        "padding": "10px",
        "margin": "0 auto",
        "whiteSpace": "nowrap",
        "marginLeft": "15%"
    }
)


layout = html.Div([
        sidebar,
        html.Div(style={"height": "150px"}),
        game_type,
        html.Div([
            html.H2(f"Selecting for team: {document['team_schedules'][TEAM_ID]['name']}", style=text_block),
            html.Img(src=document["team_schedules"][TEAM_ID]["logo"], style={"width": "15%"})
        ]),
        scrollable_row,
        dcc.Store(id='radio-values-store', data={'wins': 0, 'losses': 0}),  # Initialize counts
        html.Div(id='submit-container', style={'display': 'none', 'textAlign': 'center', 'marginTop': '20px'}, children=[
            dbc.Button("Submit", id="submit-button", color="primary")
        ]),
        html.Div(id='counts-display', style={'textAlign': 'center', 'marginTop': '20px'}),
        html.Div(style={"height": "500px"})
    ])


@callback(
    Output({"type": "card", "index": MATCH}, "style"),
    Input({"type": "radio-items", "index": MATCH}, "value"),
)
def update_card_style(selected_value):
    # Define the base style with fixed width, max-width, and height
    base_style = {
        "width": "100%", 
        "max-width": "300px", 
        "height": "300px", 
        "margin": "10px"
    }
    
    # Update the background color based on the selected value
    if selected_value == "win":
        return {**base_style, "backgroundColor": "lightgreen"}
    elif selected_value == "loss":
        return {**base_style, "backgroundColor": "lightcoral"}
    
    # Default background color if no option is selected
    return {**base_style, "backgroundColor": "white"}


@callback(
    Output('radio-values-store', 'data'),
    [Input({'type': 'radio-items', 'index': ALL}, 'value')],
    State('radio-values-store', 'data'),
    prevent_initial_call=True
)
def update_radio_values(values, current_data):
    # Update the store data with values from radio buttons
    win_count = 0
    loss_count = 0
    
    # Count wins and losses
    for value in values:
        if value == "win":
            win_count += 1
        elif value == "loss":
            loss_count += 1
    
    # Update counts in store data
    current_data['wins'] = win_count
    current_data['losses'] = loss_count
    return current_data



@callback(
    Output('submit-container', 'style'),
    Input('radio-values-store', 'data'),
    prevent_initial_call=True
)
def update_submit_button_visibility(data):
    # Check if all radio buttons have been selected
    all_selected = all(value is not None for value in data.values())
    
    if all_selected:
        return {'display': 'block', 'textAlign': 'center', 'marginTop': '20px'}
    else:
        return {'display': 'none'}
    

@callback(
    Output('counts-display', 'children'),
    Input('radio-values-store', 'data'),
    prevent_initial_call=True
)
def update_counts_display(data):
    win_count = data.get('wins', 0)
    loss_count = data.get('losses', 0)
    
    return html.Div([
        html.H4("Provisional Record:"),
        html.H2(f"{win_count}-{loss_count}")
    ])