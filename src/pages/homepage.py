# import dash
# from dash import html
# import dash_bootstrap_components as dbc

# dash.register_page(__name__, path='/')

# text_block = {
#     "textAlign": "center",
#     "font-weight": "bold",
#     "border": "2px solid white",  # White border with 2px thickness
#     "padding": "10px",  # Add some padding inside the border
#     "backgroundColor": "white",  # White background inside the border
#     "color": "black",  # Black text color for contrast
#     "border-radius": "5px",  # Optional: rounded corners
#     "display": "block",  # Use block to take full width available
#     "margin": "0 auto",  # Center the block horizontally
# } 

# layout = html.Div([
#         html.Div(style={'height': '50px'}),
#         html.Div(style={"marginTop": "100px"}),  # adds 40px vertical space
#         html.P("Look, you seem like a nice kid. Just take it easy out there, aigh?", style=text_block),
#         html.Br(),
#         html.Div(style={'height': '1000px'})
#     ],
#     style={
#         'background-image': 'url("/assets/warner.jpeg")',
#         'backgroundSize': 'cover',  # To cover the whole page
#         # 'height': '100vh',
#         'textAlign': 'center',  # Center-align text inside the container
#         'display': 'flex',  # Ensure the container uses flex layout
#         'flexDirection': 'column',  # Align items in a column
#         'justifyContent': 'center'# Center items vertically
#     }
# )
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

# Hero Section Styles
hero_style = {
    "background": "linear-gradient(135deg, #002244, #013369)",  # NFL-style navy blue gradient
    "color": "white",
    "padding": "80px 20px",
    "textAlign": "center",
    "boxShadow": "0 8px 20px rgba(0,0,0,0.3)",
}

title_style = {
    "fontSize": "3rem",
    "fontWeight": "bold",
    "textTransform": "uppercase",
    "letterSpacing": "2px",
    "animation": "fadeInDown 1s ease-out",
}

subtitle_style = {
    "fontSize": "1.5rem",
    "marginTop": "15px",
    "animation": "fadeInUp 1.5s ease-out",
}

card_style = {
    "transition": "transform 0.2s ease-in-out",
    "cursor": "pointer",
}

layout = html.Div(
    [
        html.Div(style={"marginTop": "100px"}),  # adds 40px vertical space
        # Hero Section
        html.Div(
            [
                html.H1("NFL Betting Hub", style=title_style),
                html.P(
                    "Schedules • Live Stats • Betting Insights",
                    style=subtitle_style,
                ),
            ],
            style=hero_style,
        ),

        # Feature Cards
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Upcoming Games", className="card-title"),
                                    html.P("Stay ahead with schedules and odds."),
                                ]
                            ),
                            style=card_style,
                            className="feature-card",
                        ),
                        md=4,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Live Stats", className="card-title"),
                                    html.P("Follow every play with real-time performance."),
                                ]
                            ),
                            style=card_style,
                            className="feature-card",
                        ),
                        md=4,
                    ),
                    dbc.Col(
                        dcc.Link(  # wrap the whole card
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H4("Futures", className="card-title"),
                                        html.P("Get all the future lines, all in one spot. Updated daily."),
                                    ]
                                ),
                                style=card_style,
                                className="feature-card",
                            ),
                            href="/futures",  # 👈 this routes to your futures page
                            style={"textDecoration": "none", "color": "inherit"},  # keep styling clean
                        ),
                        md=4,
                    ),
                ],
                className="g-4 my-5",
                justify="center",
            ),
            fluid=True,
        ),

        # Footer
        html.Footer(
            "⚡ Built with Dash • Data-driven NFL insights ⚡",
            style={
                "textAlign": "center",
                "padding": "20px",
                "backgroundColor": "#f8f9fa",
                "color": "#6c757d",
                "marginTop": "40px",
                "fontSize": "0.9rem",
            },
        ),
    ]
)

# Add custom CSS animations via Dash assets (assets/style.css)
# Example style.css:
"""
@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-30px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.feature-card:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
"""
