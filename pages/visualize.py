import dash
from dash import dcc, html, Input, Output, callback

dash.register_page(__name__, path="/visualise")


CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


layout = html.Div(
            [
                html.H1('Visualise Articles')
            ],
            style=CONTENT_STYLE
)