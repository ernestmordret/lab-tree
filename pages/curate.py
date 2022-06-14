import dash
from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path="/curate")

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

data_table_div = html.Div(
    [
        dash_table.DataTable(
            id='datatable-review',
            columns=[
                {"name": 'ID', "id": 'id', "deletable": False, "selectable": False},
                {"name": 'Year', "id": 'pub_year', "deletable": False, "selectable": False},
                {"name": 'Title', "id": 'title', "deletable": False, "selectable": False},
                {"name": 'Authors', "id": 'authors', "deletable": False, "selectable": False},
                {"name": 'Journal', "id": 'journal', "deletable": False, "selectable": False},
                {"name": 'Abstract', "id": 'abstract', "deletable": False, "selectable": False, 'editable': True},
                {"name": 'Link', "id": 'url', "deletable": False, "selectable": False},
                {"name": '# Citations', "id": 'num_citations', "deletable": False, "selectable": False},
                {"name": 'Reviewed', "id": 'reviewed', "deletable": False, "selectable": False, 'editable': True},
            ],
            hidden_columns=['id', 'abstract', 'url', 'authors', 'reviewed'],
            data=[],
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="single",
            row_deletable=True,
            selected_rows=[0],
            page_action="native",
            page_current=0,
            page_size=10,

            #fixed_columns={'headers': True, 'data': 2},
            style_table={
                'overflowY': 'auto',
                'overflowX': 'scroll',
                'minWidth': '100%',
                'height': '400px'
            },
            style_cell={
                # all three widths are needed
                'minWidth': '80px', 'width': '80px', 'maxWidth': '250px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{reviewed} > 0',
                    },
                    'backgroundColor': '#39CCCC',
                    'color': 'white'
                }
            ],
            css=[{"selector": ".show-hide", "rule": "display: none"}]

        ),
        html.Button(id='export-button',
                    n_clicks=0,
                    children='Export as Excel',
                    className="btn btn-primary",
                    style={'margin': '1rem'}
                    ),

        dcc.Download(id="download-dataframe-xlsx"),

        html.Hr()
    ],
    style={"padding": "2rem 1rem"}
)

review_panel = html.Div(
    [
        html.H2('Link to publication'),
        dcc.Link(href='', id='pub-link', target="_blank"),

        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H1('Abstract'),
                            dcc.Textarea(
                                id='abstract-textarea',
                                value='Select an article to reveal its abstract',
                                style={'width': '100%', 'height': 300}
                            )
                        ]
                    ),
                    width={"size": 8, "order": 0, "offset": 0}
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H1('Authors'),
                            dcc.Dropdown(
                                id='authors-dropdown',
                                options=[],
                                value=[],
                                multi=True,
                                style={'height': 300}
                            )
                        ]
                    ),
                )

            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H1('Keywords'),
                            dcc.Dropdown(
                                id='keywords-dropdown',
                                options=[],
                                value=[],
                                multi=True,
                            )
                        ],
                    ),
                    width={"size": 8, "order": 0, "offset": 0}
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H3('add new keyword'),
                            dcc.Input(id='input-new-keyword', type='text'),
                            html.Button(id='button-new-keyword',
                                        n_clicks=0,
                                        children='Add option',
                                        className="btn btn-primary",
                                        style={'margin': '1rem'}
                                        )

                        ]
                    )
                )
            ]
        ),

        html.Button(id='reviewed-button',
                    n_clicks=0,
                    children='Mark as reviewed',
                    className="btn btn-primary",
                    style={'margin': '1rem'}
                    ),
        html.Button(id='fetch-author-button',
                    n_clicks=0,
                    hidden=True
                    ),
        html.Button(id='load-demo-button',
                    n_clicks=0,
                    hidden=True
                    ),
        html.Button(id='input-name-load',
                     n_clicks=0,
                     hidden=True
                    ),
        dcc.Upload(id='upload-excel')

    ])

layout = dbc.Col([
    dbc.Row([data_table_div]),
    dbc.Row([review_panel]),
],
    style=CONTENT_STYLE)


# REVIEW CALLBACKS

@callback(Output("datatable-review", "data"),
          Output("authors-dropdown", "options"),
          Input("store-data", "data"),
          Input("reviewed-button", "n_clicks"),
          Input("fetch-author-button", "n_clicks")
)
def populate_datatable(data, n_clicks, n_clicks2):
    df = pd.DataFrame.from_records(data)
    authors_options = list(set(sum([i.split('|') for i in df.authors.values],[])))
    return df.to_dict('records'), authors_options



# Update the abstract when a new row is selected
@callback(
    Output('abstract-textarea', 'value'),
    State('datatable-review', 'data'),
    Input('datatable-review', 'selected_rows')
)
def update_abstract(data, selected_rows):
    if selected_rows:
        i = selected_rows[0]
        if data:
            new_abstract = data[i]['abstract']
            return new_abstract
    return ''


# Update the authors list when a new row is selected
@callback(
    Output('authors-dropdown', 'value'),
    State('datatable-review', 'data'),
    Input('datatable-review', 'selected_rows')
)
def update_authors_list(data, selected_rows):
    if selected_rows:
        i = selected_rows[0]
        if data:
            authors_list = data[i]['authors'].split('|')
            return authors_list
    return []


# Update the publication link when a new row is selected
@callback(
    Output('pub-link', 'href'),
    State('datatable-review', 'data'),
    Input('datatable-review', 'selected_rows')
)
def update_pub_link(data, selected_rows):
    if selected_rows:
        i = selected_rows[0]
        if data:
            return data[i]['url']
    return ''


# Add a new keyword via the input
@callback(
    Output('keywords-dropdown', 'options'),
    Input('button-new-keyword', 'n_clicks'),
    State('input-new-keyword', 'value'),
    State('keywords-dropdown', 'options')
)
def update_keywords(n_clicks, new_value, current_options):
    if n_clicks:
        options = set(current_options)
        options.add(new_value)
        new_options = list(options)
        return new_options
    return current_options


# store-other update
@callback(
    Output('store-others', 'data'),
    Input('datatable-review', 'selected_rows'),
    Input('abstract-textarea', 'value'),
    State('store-others', 'data'),
    prevent_initial_call=True
)
def update_others(selected_rows, new_abstract, other_data):
    new_data = other_data.copy()
    new_data['selected_rows'] = selected_rows
    new_data['abstract'] = new_abstract
    return new_data

# update middleman
@callback(
    Output('middleman', 'data'),
    Input('datatable-review', 'data_timestamp'),
    State('datatable-review', 'data'),
    State('datatable-review', 'data_previous')
)
def update_middleman_upon_row_delete(ts, data, data_previous):
    if ts:
        if data_previous:
            if len(data) == len(data_previous) - 1:
                return data
    return dash.no_update

# export data as excel
@callback(
    Output('download-dataframe-xlsx', "data"),
    Input('export-button', 'n_clicks'),
    State('store-data', 'data')
)
def export_data(n_clicks, data):
    if n_clicks>0:
        df = pd.DataFrame.from_records(data)
        return dcc.send_data_frame(df.to_excel, "my_export.xlsx")

