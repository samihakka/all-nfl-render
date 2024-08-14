import dash
from dash import dcc, html, Input, Output, callback, State, dash_table, MATCH
import pandas as pd
from helpers.mongo_support import MongoConnect
import plotly.graph_objects as go
import dash_bootstrap_components as dbc



class BettingHelper():

    def __init__(self) -> None:
        pass

    def say_hi(self):
        print("hey!")
        return None

    def build_bar_graph(self, selected_team, team_id_dic, logs, logo):

        weeks = [d["week"] for d in logs]
        over_under_values = [d["over/under"] for d in logs]
        df = pd.DataFrame({
            "Week": weeks,
            "Over/Under": over_under_values
        })
        # bye_week = None

        # for i, week in enumerate(weeks, start=1):
        #     if i != week:
        #         bye_week = i
        #         break

        average_over_under = df["Over/Under"].mean()

        fig = go.Figure(data=[
            go.Bar(x=df["Week"], y=df["Over/Under"], name="Over/Under")
        ])

        fig.add_shape(
            type="line",
            x0=0,
            x1=max(weeks),
            y0=average_over_under,
            y1=average_over_under,
            line=dict(color="Red", width=2, dash="dot"),
            xref="x",
            yref="y"
        )

        # if bye_week:
        #     print(bye_week)
        #     fig.add_trace(go.Bar(
        #             x=bye_week,
        #             y=60,  # Placeholder value for the bye week
        #             name="Over/Under",
        #             marker_color='grey'
        #         ))

        fig.update_layout(
            title=f"Over/Under Values by Week for {selected_team}",
            xaxis_title="Week",
            yaxis_title="Over/Under",
            template="plotly_white",
            yaxis=dict(
                range=[25, 60]  # Set the y-axis range from 30 to 60
            )
        )

        fig2 = dcc.Graph(id='my-graph', figure=fig, style={'width': "100%"})
        layout = [dcc.Store(id='my-figure'), fig2, html.Img(src=logo,id="graph-logo",style={"width": "15%" })]
        return layout



    def build_bar_graph_spread(self, selected_team, team_id_dic, logs, logo):

        weeks = [d["week"] for d in logs]
        spread_values = [float(d["spread"]) for d in logs]
        df = pd.DataFrame({
            "Week": weeks,
            "Spread": spread_values
        })
        # bye_week = None

        # for i, week in enumerate(weeks, start=1):
        #     if i != week:
        #         bye_week = i
        #         break

        average_spread = df["Spread"].mean()

        fig = go.Figure(data=[
            go.Bar(x=df["Week"], y=df["Spread"], name="Spread")
        ])

        fig.add_shape(
            type="line",
            x0=0,
            x1=max(weeks),
            y0=average_spread,
            y1=average_spread,
            line=dict(color="Red", width=2, dash="dot"),
            xref="x",
            yref="y"
        )

        # if bye_week:
        #     print(bye_week)
        #     fig.add_trace(go.Bar(
        #             x=bye_week,
        #             y=60,  # Placeholder value for the bye week
        #             name="Over/Under",
        #             marker_color='grey'
        #         ))

        fig.update_layout(
            title=f"Spread Values by Week for {selected_team}",
            xaxis_title="Week",
            yaxis_title="Spread",
            template="plotly_white",
            yaxis=dict(
                range=[-15, 15]  # Set the y-axis range from 30 to 60
            )
        )

        fig2 = dcc.Graph(id='my-graph-2', figure=fig, style={'width': "100%"})
        layout = [dcc.Store(id='my-figure-2'), fig2, html.Img(src=logo,id="graph-logo-2",style={"width": "15%" })]
        return layout





    def load_ou_page(self, team_id_dic):

        ou_dropdown_options = [{"label": key, "value": key} for key in team_id_dic.keys()]

        ou_dropdown = dcc.Dropdown(
            id="ou-dropdown",
            options=ou_dropdown_options,
            placeholder="Select a team",
            value="ARI",
            style={"width": "50%"}  # Adjust width as needed
        )

        layout = html.Div([

            html.H1("BIIITCH WE HITTIN THE OVER!!!", style={"text-align": "center"}),
            ou_dropdown,
            html.Div(id='bar-graph-container', style={'margin': '0 7%'}),
            ]
        )

        return layout
    


    def load_spread_page(self, team_id_dic, team_spreads):

        ou_dropdown_options = [{"label": key, "value": key} for key in team_id_dic.keys()]

        spread_dropdown = dcc.Dropdown(
            id="spread-dropdown",
            options=ou_dropdown_options,
            placeholder="Select a team",
            value="ARI",
            style={"width": "50%"}  # Adjust width as needed
        )


        top_5 = list(team_spreads.items())[:5]
        rows = []
        for team_id, team_data in top_5:
            print("team_id:", team_id)
            print("team data:", team_data)
            rows.append(
                dbc.Row(
                    [dbc.Col(html.Div(f"{team_id}")),
                    dbc.Col(html.Div(f"{team_data}"))],

                )
            )

        bottom_5 = list(team_spreads.items())[-5:]
        bottom_5 = reversed(bottom_5)
        bad_rows = []
        for team_id, team_data in bottom_5:
            print("team_id:", team_id)
            print("team data:", team_data)
            bad_rows.append(
                dbc.Row(
                    [dbc.Col(html.Div(f"{team_id}")),
                    dbc.Col(html.Div(f"+{team_data}"))],

                )
            )

        card = dbc.Card(
            [
                dbc.CardHeader("Top 5 Teams"),
                dbc.CardBody(rows)
            ],
            body=True,
            style={"width": "18rem"}
        )
        card2 = dbc.Card(
            [
                dbc.CardHeader("BOTTOM 5 Teams"),
                dbc.CardBody(bad_rows)
            ],
            body=True,
            style={"width": "18rem"}
        )

        layout = html.Div([

            html.H1("SPREAD YA LEGS!!!", style={"text-align": "center"}),
            spread_dropdown,
            html.Div(id='bar-graph-container-spread', style={'margin': '0 7%'}),
            dbc.Row(
                [dbc.Col(card, width="auto"),
                dbc.Col(card2, width="auto")]
                
            )
        ])

        return layout

