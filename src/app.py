import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc


# Initialize the Dash app
dbc_css = 'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css'
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True, use_pages=True)
server = app.server

# import full_season_team_stats

app.title = "NFL is King"
black="0a0a0a"

nav = dbc.Nav([
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem("Simple Stuff", href="/once-per"),
            dbc.DropdownMenuItem("Advanced Betting", href="/betting-advanced"),
        ],
        label="Betting",
        nav=True
    ),
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem("Team Stats", href="/full-season-team-stats"),
            dbc.DropdownMenuItem("League Leaders", href="/league-leaders"),
        ],
        label="Stats",
        nav=True
    )
])

NFL_logo = "assets/trans_nfl_logo.png"
steamers = "assets/trans_duke.png"

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=NFL_logo, height="100px")),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "All-NFL Dashboard",
                                className="ms-1",
                                style={"font-size": "2rem", 'font-weight': 'bold'}  # Increase font size
                            )
                        ),
                        dbc.Col(html.Img(src=steamers, height="100px")),
                    ],
                    align="center",
                    className="g-0",
                    style={"margin": "0 auto"}
                ),
                href="/",
                style={"textDecoration": "none"}
            ),
            nav,
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)
        ]
    ),
    style={
        "background": "linear-gradient(to right, #2847f7, #fa4141)"  # Gradient colors 
    },
    dark=True
)

app.layout = html.Div([
    navbar,
    # html.H1("Beep Boop", style={"textAlign": 'center'}),
    dcc.Location(id='url', refresh=False),  # Manages URL
    dash.page_container
])


if __name__ == '__main__':
    app.run_server(debug=True)