from scholarly import scholarly


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
    return f"Started fetching author and publications", {'author': author}


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
        return 100 * (n_filled + 1) / L, new_list
    return dash.no_update, dash.no_update
