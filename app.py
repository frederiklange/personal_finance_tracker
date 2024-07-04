# Import packages
from dash import Dash, html, dash_table, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Incorporate data
transactions_df = pd.read_csv("data/clean/transactions_clean.csv")
expenditure = (
    transactions_df[transactions_df["expenditure"] == 1]
    .groupby("month")
    .agg({"transaction_amount": "sum"})["transaction_amount"]
)
income = (
    transactions_df[transactions_df["expenditure"] == 0]
    .groupby("month")
    .agg({"transaction_amount": "sum"})["transaction_amount"]
)
months = transactions_df["month"].unique()
avg_expenditure = [expenditure.sum() / len(months)] * len(months)
avg_income = [income.sum() / len(months)] * len(months)

# Creating figures
fig = go.Figure(
    data=[
        go.Bar(name="Expenditures", x=months, y=expenditure, marker_color="#8839ef"),
        go.Bar(name="Income", x=months, y=income, marker_color="#7287fd"),
        go.Scatter(
            name="Average Expenditure",
            x=months,
            y=avg_expenditure,
            mode="lines",
            line=dict(color="#8839ef", width=2, dash="dash"),
        ),
        go.Scatter(
            name="Average Income",
            x=months,
            y=avg_income,
            mode="lines",
            line=dict(color="#7287fd", width=2, dash="dash"),
        ),
    ],
    layout=go.Layout(
        title=go.layout.Title(text="Monthly Expenditures and Income (DKK)"),
        yaxis=dict(tickformat=",.0f"),
        template="simple_white",
    ),
)

fig.update_layout(
    barmode="group",
    width=990,
    height=600,
    legend={"orientation": "h", "y": -0.2, "x": 0.2},
)

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# App layout
app.layout = dbc.Container(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H1(children="Personal Finances Dashboard"),
                        html.P(
                            children="This dashboards provides an overview of my personal finances to quickly navigate expenses, income and stocks."
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.H2(
                            children="Expenditures and Income", style={"margin-top": 50}
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Div(
                            dbc.RadioItems(
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-light",
                                labelCheckedClassName="btn btn-light",
                                options=[
                                    {"label": "Graph", "value": 1},
                                    {"label": "Table", "value": 2},
                                ],
                                value=1,
                                style={"width": "100%"},
                            ),
                            style={"width": 340},
                        ),
                    ],
                    style={"margin-left": 15, "margin-right": 15, "display": "flex"},
                ),
                html.Div(
                    [
                        html.H2(children="Shares", style={"margin-top": 50}),
                    ]
                ),
                html.Div(
                    [
                        html.Div(
                            dbc.RadioItems(
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-light",
                                labelCheckedClassName="btn btn-light",
                                options=[
                                    {"label": "Graph", "value": 1},
                                    {"label": "Table", "value": 2},
                                ],
                                value=1,
                                style={"width": "100%"},
                            ),
                            style={"width": 340},
                        ),
                    ],
                    style={"margin-left": 15, "margin-right": 15, "display": "flex"},
                ),
            ],
            style={
                "width": 340,
                "margin-left": 35,
                "margin-top": 35,
                "margin-bottom": 35,
            },
            className="dashboard-sidebar",
        ),
        html.Div(
            [
                dcc.Graph(figure=fig),
            ],
            style={
                "width": 990,
                "margin-top": "auto",
                "margin-right": 35,
                "margin-bottom": "auto",
            },
        ),
    ],
    fluid=True,
    style={"display": "flex"},
    className="dashboard-container",
)

# Callbacks


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
