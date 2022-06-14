import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, dash_table, callback, long_callback
import pandas as pd
import io
import base64
from dash.long_callback import DiskcacheLongCallbackManager
import diskcache
from dash.exceptions import PreventUpdate
from utils import *

cache = diskcache.Cache('./cache')
lcm = DiskcacheLongCallbackManager(cache)

app = dash.Dash(
    __name__,
    plugins=[dl.plugins.pages],
    external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css'],
    long_callback_manager=lcm,
    suppress_callback_exceptions=True
)

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
                dbc.NavLink("Curate articles", href="/curate", disabled=True, id='navlink-curate'),
                dbc.NavLink("Visualise", href="/visualise", disabled=True, id='navlink-visualise'),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = dbc.Container(
    [sidebar,
     dcc.Store(id='store-data', data=[]),
     dcc.Store(id='store-others', data={
                                        'selected_rows': [],
                                        'abstract': '',
                                        'active_curate':False,
                                        'active_visualize':False,
                                    }),
     dcc.Store(id='middleman', data=[]),
     dcc.Store(id='context', data='spurious'),
     dl.plugins.page_container],
)


@callback(
    Output('context', 'data'),
    Input('fetch-author-button', 'n_clicks'),
    Input('reviewed-button', 'n_clicks'),
    Input('load-demo-button', 'n_clicks'),
    Input('middleman', 'data'),
    Input('upload-excel', 'contents'),
    prevent_initial_call=True
)
def callback_buttons(n_click_fetch,
                     n_click_reviewed,
                     n_click_load_demo,
                     middle_data,
                     upload_excel_contents):
    ctx = dash.callback_context
    ctrl_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if ctrl_id == 'fetch-author-button':
        if n_click_fetch > 0:
            return ctrl_id

    if ctrl_id == 'reviewed-button':
        if n_click_reviewed > 0:
            return ctrl_id

    if ctrl_id == 'load-demo-button':
        if n_click_load_demo > 0:
            return ctrl_id

    if ctrl_id in ['middleman', 'upload-excel']:
        return ctrl_id

    return dash.no_update


@app.long_callback(
    output=Output('store-data', 'data'),
    inputs=(Input('context', 'data'),
            State('store-others', 'data'),
            State('store-data', 'data'),
            State('input-name-load', 'value'),
            State('middleman', 'data'),
            State('upload-excel', 'contents')),
    running=[(Output('fetch-author-button', 'disabled'), True, False)],
    prevent_initial_call=True

)
def update_data(context, other_data, data,
                author_name, middleman_data, uploaded_excel):

    if context == 'load-demo-button':

        df = pd.read_csv('datasets/Naama.tsv', sep='\t')
        df['reviewed'] = False
        df.sort_values('pub_year', ascending=True, inplace=True)
        data = df.to_dict('records')
        return data

    if context == 'reviewed-button':
        if data:
            if other_data['selected_rows']:
                i = other_data['selected_rows'][0]
                data[i]['abstract'] = other_data['abstract']
                data[i]['reviewed'] = True
        return data

    if context == 'upload-excel':
        if uploaded_excel:
            content = uploaded_excel[0]
            _, content_string = content.split(',')
            decoded = base64.b64decode(content_string)
            df = pd.read_excel(io.BytesIO(decoded))
            data = df.to_dict('records')
            return data

    if context == 'fetch-author-button':
        if author_name and not data:
            print(author_name)
            data = fetch_author(author_name)
            return data

    if context == 'middleman':
        return middleman_data


@callback(
    Output('navlink-curate', 'disabled'),
    Input('store-data', 'data')
)
def activate_curate(data):
    if data:
        return False
    return dash.no_update


if __name__ == "__main__":

    app.run_server(debug=True)
