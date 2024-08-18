import dash
from dash import dcc, html, Input, Output, callback, State, dash_table, MATCH
import pandas as pd
from helpers.mongo_support import MongoConnect
import dash_bootstrap_components as dbc

mongo = MongoConnect()

dash.register_page(__name__, path='/schedule-game')
sandbox = ["display", "logo", "logo_html"]

document = mongo.load_with_year("schedule_predict", 2024)

niners = document["team_schedules"]["25"]

print("YAYAYAYAYAYAYYAYAYAYAAYAYAYAYAYAYYAAYAYAYAYAYYAYAYA")
print(niners)

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
    style={"width": "100%", "max-width": "70%", "margin": "20px auto"}
    )
    return card


# Create the cards
niners_cards_arr = [create_single_card(blank) for blank in niners["schedule"]]

# Split the cards into rows with a maximum of 4 cards per row
rows = []
for i in range(0, len(niners_cards_arr), 4):
    row = dbc.Row(
        [dbc.Col(card, width=3) for card in niners_cards_arr[i:i+4]],
        className="mb-4"
    )
    rows.append(row)

layout = html.Div([
    html.Div(style={"height": "150px"}),  # Placeholder for spacing
    *rows,  # Unpack the rows into the layout
])


@callback(
    Output({"type": "card", "index": MATCH}, "style"),
    Input({"type": "radio-items", "index": MATCH}, "value"),
)
def update_card_style(selected_value):
    if selected_value == "win":
        return {"backgroundColor": "lightgreen", "width": "100%", "max-width": "70%", "margin": "20px auto"}
    elif selected_value == "loss":
        return {"backgroundColor": "lightcoral", "width": "100%", "max-width": "70%", "margin": "20px auto"}
    return {"backgroundColor": "white", "width": "100%", "max-width": "70%", "margin": "20px auto"}
