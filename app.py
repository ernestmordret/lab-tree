import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, dash_table, callback
import pandas as pd
import io
import base64

app = dash.Dash(
    __name__,
    plugins=[dl.plugins.pages],
    external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css'],
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
     dl.plugins.page_container],
)


@callback(
    Output('store-data', 'data'),
    Input('fetch-author-button', 'n_clicks'),
    Input('reviewed-button', 'n_clicks'),
    Input('load-demo-button', 'n_clicks'),
    State('store-others', 'data'),
    State('store-data', 'data'),
    Input('middleman', 'data'),
    Input('upload-excel', 'contents'),
    prevent_initial_call=True

)
def update_data(n_click_load,  n_clicks_reviewed, n_clicks_demo,  other_data,  data,
                middleman_data, uploaded_excel):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'load-demo-button':
        if n_clicks_demo > 0:
            df = pd.read_csv('datasets/Naama.tsv', sep='\t')
            df['reviewed'] = False
            df.sort_values('pub_year', ascending=True, inplace=True)
            records = df.to_dict('records')
            print(f"update_data, triggered by : {trigger_id}")
            return records

    if trigger_id == 'reviewed-button':
        if n_clicks_reviewed > 0:
            print(f"update_data, triggered by : {trigger_id}")
            if data:
                print(other_data)
                if other_data['selected_rows']:
                    i = other_data['selected_rows'][0]
                    print(i)
                    data[i]['abstract'] = other_data['abstract']
                    data[i]['reviewed'] = True
        return data

    if trigger_id == 'upload-excel':
        content = uploaded_excel[0]
        _, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_excel(io.BytesIO(decoded))
        records = df.to_dict('records')
        return records

    if trigger_id == 'middleman':
        return middleman_data

    return dash.no_update

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
