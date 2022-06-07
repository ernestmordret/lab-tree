import dash
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

input_load = dcc.Input(id='input-name-load', type='text')

fetch_author_button = html.Button(id='fetch-author-button',
                                 n_clicks=0,
                                 children="Fetch author's publications",
                                 className="btn btn-primary",
                                 style={'margin': '1rem'}
                                 )

reviewed_button = html.Button(id='reviewed-button',
            n_clicks=0,
            hidden=True
            )

load_from_excel_button = html.Button(id='load-from-excel-button',
            n_clicks=0
            )


layout = dbc.Col([
    dbc.Row(
        dbc.Col(html.Div(children="Type the name of your favorite researcher"), width=6),
        justify="center"
    ),
    dbc.Row(
        dbc.Col(html.Div([input_load, fetch_author_button, reviewed_button]), width=6),
        justify="center",
        align="center",
    ),
],
    style=CONTENT_STYLE
)


