import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, dash_table
import pandas as pd
from scholarly import scholarly
            
 
app = dash.Dash(external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css'],
               suppress_callback_exceptions=True)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Lab Tree", className="display-4"),
        html.Hr(),
        html.P(
            "A simple tool to annotate an author's publications and visualise them", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Load articles", href="/", active="exact"),
                dbc.NavLink("Review articles", href="/review", active="exact"),
                dbc.NavLink("Visualise", href="/visualise", disabled=True),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

########################################################################
# LOAD COMPONENTS
########################################################################

data_store = dcc.Store(id='data-store', data={})
pub_store = dcc.Store(id='filled-pub-store', data=[])
interval_checker = dcc.Interval(
            id='interval-checker',
            interval=1*2000, # in milliseconds
            n_intervals=0,
            disabled=True
        )
input_load = dcc.Input(id='input-name-load', type='text')
submit_button_load = html.Button(id='submit-button-load', 
                                 n_clicks=0, 
                                 children='Fetch author', 
                                 className="btn btn-primary", 
                                 style={'margin':'1rem'}
                                )
output_load = html.Div(id='output-load')
loading = dbc.Spinner(color="primary", id='loading-1', children=' ')
progress = dbc.Progress(value=0, id='progress-load')

next_pub_button = html.Button(id='next-pub-button', 
                                 n_clicks=0, 
                                 hidden=True, 
                                )

########################################################################
# REVIEW COMPONENTS
########################################################################

df = pd.read_csv('pickles/Naama.tsv', sep='\t')
df['reviewed'] = False
df.sort_values('pub_year', ascending=True, inplace = True)

authors_options = list(set.union(*[set(eval(i)) for i in df['authors']]))


['New York City', 'Montreal', 'San Francisco']
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
                {"name": 'Abstract', "id": 'abstract', "deletable": False, "selectable": False, 'editable':True},
                {"name": 'Link', "id": 'url', "deletable": False, "selectable": False},
                {"name": '# Citations', "id": 'num_citations', "deletable": False, "selectable": False},
                {"name": 'Reviewed', "id": 'reviewed', "deletable": False, "selectable": False, 'editable':True},
            ],
            hidden_columns = ['id','abstract', 'url', 'authors', 'reviewed'],
            data=df.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="single",
            row_deletable=True,
            selected_rows=[0],
            page_action="native",
            page_current=0,
            page_size= 10,

            fixed_columns={ 'headers': True, 'data': 2 },
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
        html.Hr()
   ],
    style = {"padding": "2rem 1rem"}
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
                                options=authors_options,
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
                                         style={'margin':'1rem'}
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
                    style={'margin':'1rem'})

   ],
    style = {"padding": "2rem 1rem"}
)






@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    
    if pathname == "/":
        
        page_layout = dbc.Col([
                dbc.Row(
                    dbc.Col(html.Div(children="Type the name of your favorite researcher"), width=6),
                    justify="center"
                ),
                dbc.Row(
                    dbc.Col(html.Div([input_load,submit_button_load]), width=6),
                    justify="center",
                    align="center",
                ),
                dbc.Row(
                    dbc.Col(html.Div([loading,output_load]), width=6, align="center"),
                    justify="center",
                    align="center",
                ),
                dbc.Row(
                    dbc.Col(html.Div([pub_store, data_store, interval_checker, progress]), width=6, align="center"),
                    justify="center",
                    align="center",
                ),
            ],
        )
                
        return page_layout
    
    
    elif pathname == "/review":

        page_layout = dbc.Col([
                dbc.Row([data_table_div]),
                dbc.Row([review_panel]),
        ],
        style = {"padding": "2rem 1rem"})

        return page_layout
            
        
        
    elif pathname == "/visualise":
        return html.P("Oh cool, let's look at the data!")
    # If the user tries to reach a different page, return a 404 message
    
    
    jumbotron = html.Div(
        dbc.Container(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ],
            fluid=True,
            className="py-3",
        ),
        className="p-3 bg-light rounded-3",
    )
    
    
    return jumbotron



#####
# THIS IS A PLAN:
# load a publication --> update the progress bar, and call author.load(). Not sure it works, unless a 
# component increments itself via a callback, and iterates through the pub loop at the same time
# try : dcc.Store(id='my-store', data={'my-data': 'data'})


# LOAD CALLBACKS
@app.callback(Output('loading-1', 'children'),
              Output('data-store', 'data'),
              Input('submit-button-load', 'n_clicks'),
              State('input-name-load', 'value'),
              
              prevent_initial_call=True
             )
def fetch_author(n_clicks, name):

    search_query = scholarly.search_author(name)
    first_author_result = next(search_query)
    author = scholarly.fill(first_author_result)
    author['pub_index'] = 0
    return f"Started fetching author and publications", {'author':author}

        
    
@app.callback(Output("progress-load", "value"),
              Output('filled-pub-store', 'data'),
              Input('data-store', 'data'),
              Input('filled-pub-store', 'data'),
              prevent_initial_call=True
             )
def load_pub(data, filled_pub_list):
    
    author = data['author']
    publications = author['publications']
    n_filled = len(filled_pub_list)
    L = len(publications)
    if n_filled != L:
        pub = publications[n_filled]
        filled_pub = scholarly.fill(pub)
        new_list = filled_pub_list.copy() + [filled_pub]
        return 100*(n_filled+1)/L,  new_list
    return dash.no_update, dash.no_update
    
@app.callback(Output('interval-checker', 'disabled'),
              Input('interval-checker', 'n_intervals'),
              Input('filled-pub-store', 'data'),
              Input('data-store', 'data')
             )
def disable_ticker(n_intervals, filled_pub_list, data):
    
    ctx = dash.callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id in ['filled-pub-store', 'data-store']:
            return False # a new pub was added, or the auhtor was updated --> the ticker should tick
        return True # the ticker has ticked, it should be disabled
    return True # if it was not triggered, the ticker should remain disabled

    
# REVIEW CALLBACKS
# Update the abstract when a new row is selected
@app.callback(
    Output('abstract-textarea', 'value'),
    State('datatable-review', 'data'),
    Input('datatable-review', 'selected_rows')
)
def update_abstract(data, selected_rows):
    if selected_rows:
        i = selected_rows[0]
        new_abstract = data[i]['abstract']
        if new_abstract:
            return new_abstract
        else:
            return ''

        
# Update the authors list when a new row is selected
@app.callback(
    Output('authors-dropdown', 'value'),
    State('datatable-review', 'data'),
    Input('datatable-review', 'selected_rows')
)
def update_abstract(data, selected_rows):
    if selected_rows:
        i = selected_rows[0]
        authors_list = eval(data[i]['authors'])
        if authors_list:
            return authors_list
        else:
            return []

        
# Update the publication link when a new row is selected
@app.callback(
    Output('pub-link', 'href'),
    State('datatable-review', 'data'),
    Input('datatable-review', 'selected_rows')
)
def update_pub_link(data, selected_rows):
    if selected_rows:
        i = selected_rows[0]
        return data[i]['url']
    return ''


# Add a new keyword via the input
@app.callback(
    Output('keywords-dropdown', 'options'),
    Input('button-new-keyword', 'n_clicks'),
    State('input-new-keyword', 'value'),
    State('keywords-dropdown', 'options')
)
def update_keywords(n_clicks,new_value,current_options):
    if n_clicks:
        options = set(current_options)
        options.add(new_value)
        new_options = list(options)
        return new_options
    return current_options
            
            
# Mark as reviewed
@app.callback(
    Output('datatable-review', 'data'),
    Input('reviewed-button', 'n_clicks'),
    State('datatable-review', 'selected_rows'),
    State('abstract-textarea', 'value'),
    State('datatable-review', 'data'),
    prevent_initial_call=True
    
)
def update_abstract(n_click, selected_rows, new_abstract, data):
    if n_click >0 :
        i = selected_rows[0]
        new_data = data.copy()
        new_data[i]['abstract'] = new_abstract
        new_data[i]['reviewed'] = True
        return new_data



if __name__ == "__main__":
    app.run_server(port=8899, debug=True)
