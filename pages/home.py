import dash
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

input_load = dcc.Input(id='input-name-load', type='text', placeholder="")

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

upload_from_excel = dcc.Upload(
                            id='upload-excel',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            # Allow multiple files to be uploaded
                            multiple=True
                        )

load_demo_button = html.Button(id='load-demo-button',
                                 n_clicks=0,
                                 children="Load the demo dataset",
                                 className="btn btn-primary",
                                 style={'margin': '1rem'}
                                 )

update_context_button = html.Button(id='update-context',
                                    n_clicks=0,
                                    hidden=True),


layout = dbc.Col(
    [

        dbc.Row(
            dbc.Col(html.H3(children="Type the name of your favorite researcher"), width=6),
            justify="center"
        ),

        dbc.Row(
            dbc.Col(html.Div([input_load, fetch_author_button, reviewed_button]), width=6),
            justify="center",
            align="center",
        ),

        html.Hr(),

        dbc.Row(
            dbc.Col(html.H3(children="Load a previous export"), width=6),
            justify="center"
        ),

        dbc.Row(
            dbc.Col(html.Div([upload_from_excel]), width=6),
            justify="center"
        ),

        html.Hr(),

        dbc.Row(
            dbc.Col(html.H3(children="Load demo – Naama Barkai"), width=6),
            justify="center"
        ),

        dbc.Row(
            dbc.Col(load_demo_button, width=6),
            justify="center",
            align="center",
        ),


    ],
    style=CONTENT_STYLE
)


