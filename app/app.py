"""
About:

The purpose of this project is to use Dash to allow users to 
1. Create tabs as desired
2. Delete specific tabs
3. Refresh the application and have the state of tabs created and destroyed preserved

Here the dcc.Store component is used to store tab elements, as well as other 
data that needs persistence. 

Next steps to enhance usability, users should:
4. Have editable content living on individual tabs preserved through refresh.
To achieve (4), this may involve multiple instances of the dcc.Store, residing on 
created Tabs, with pattern-matching IDs.

"""
from dash import (
    dcc,
    html,
    Dash,
    Input,
    Output,
    State,
    dash_table,
    MATCH,
    ALL,
    callback_context,
    _utils
)
import pandas as pd

def create_app():

    df = pd.DataFrame({'a':[1,2,3],
                       'b':[4,5,6]})
    app = Dash(__name__)

    app.layout = html.Div(
            id='full-app',
            children = [
                dcc.Store('tab-store',storage_type='session'),
                dcc.Store('table-store',storage_type='session'),
                dcc.Store('full-table-object-store',storage_type='session'),
                dcc.Store('clicks-store',storage_type='session'),
                html.Div(
                        id='table-div',
                        children = [
                        dash_table.DataTable(
                        id='data-table',
                        data = df.to_dict('records'),
                        columns = [{"name": i, "id": i} for i in df.columns],
                        editable=True
                        ),
                        ]),
                html.Div(id='debugger'),
                html.Button('Add Tab', id='add-tab', n_clicks=0),
                html.Div(
                        id='tab-div',
                        children = [
                        dcc.Tabs(id='tabs-container',
                        children = [
                        ]
                        )
                        ]
                    )   
            ]
        )

    # Callbacks to save updated data
    # 1. On data change, save to store data
    # 2. On store modified TS change, load stored data if available, else load current data
    @app.callback(
            #Output('table-store', 'data'), 
            Output('full-table-object-store', 'data'), 
            [
            #Input('data-table', 'data'),
            Input('table-div', 'children'),
            Input('table-div', 'n_clicks'),
            ]
            )
    def save_main_table(data,ts):
        return data
    
    @app.callback(
            #Output('data-table', 'data'), 
            Output('table-div', 'children'), 
            [
            #Input('table-store', 'modified_timestamp'),
            Input('full-table-object-store', 'modified_timestamp'),
            ],
            [
            #State('table-store', 'data'),
            State('full-table-object-store', 'data'),
            #State('data-table', 'data'),
            State('table-div', 'children'),
            ]
            )
    def retrieve_saved_table(ts,saved_data,current_data):

        if saved_data is not None:
            return saved_data
        
        return current_data
    
    # Callbacks to save updated n_clicks
    @app.callback(
            Output('clicks-store', 'data'), 
            [
            Input('add-tab', 'n_clicks'),
            ]
            )
    def save_add_tab_n_clicks(n_clicks):
        return n_clicks
    
    @app.callback(
            Output('add-tab', 'n_clicks'), 
            [
            Input('clicks-store', 'modified_timestamp'),
            ],
            [
            State('clicks-store', 'data'),
            State('add-tab', 'n_clicks'),
            ]
            )
    def retrieve_add_tab_n_clicks(ts,saved_n_clicks,current_n_clicks):

        if saved_n_clicks is not None:
            return saved_n_clicks
        
        return current_n_clicks
    
    
    # IF TAB CONTAINER CHILDREN CHANGED, ADD TO TAB STORE
    @app.callback([Output('tab-store', 'data')], 
                  [
                    Input('tabs-container', 'children'),
                   ])
    def save_tabs(children):
        return [children]
    
    # LOAD EXISTING CHILDREN FROM TAB STORE, ADD OR DELETE, PUSH TO TAB CONTAINER
    @app.callback(
        [Output('tabs-container','children'),
         Output('debugger','children')],
        [Input('add-tab','n_clicks'),
        Input({'type':'delete-tab','index':ALL},'n_clicks')],
        [State('tab-store','data')]
    )
    def add_tab(n_clicks,delete_n_clicks,existing_children):

        # RECORD ID OF ELEMENT THAT TRIGGERED CALLBACK
        trigger = callback_context.triggered_id


        children=existing_children or []

        #IF N_CLICKS IS TRIGGER, AND N_CLICKS TAB DOESN'T EXIST, APPEND IT TO CHILDREN
        if (n_clicks>0):

            new_id = f"tab-{n_clicks}"
            id_elems = [elem['props']['id'] 
                        for elem in children 
                        if 'id' in elem['props'].keys()]

            if new_id not in id_elems:
                children.append(
                    dcc.Tab(
                    id=new_id,
                    label=f"Tab {n_clicks}",
                    children=[
                        html.P(f"This is Tab {n_clicks}"),
                        html.P(str(trigger)),
                        dash_table.DataTable(
                        id=f'data-table-{n_clicks}',
                        data = df.to_dict('records'),
                        columns = [{"name": i, "id": i} for i in df.columns],
                        editable=True
                        ),
                        html.Button("Delete Tab",
                                    id={'type':'delete-tab','index':n_clicks},
                                    n_clicks=0)
                    ]
                    )
                )

        # IF TRIGGER IS DELETION, DELETE THE ITH TAB FROM CHILDREN
        if type(trigger)==_utils.AttributeDict:
            if trigger['type']=='delete-tab':
                children = [
                    tab
                    for tab in children
                    if tab['props']['id'] != f"tab-{trigger['index']}"
                ]
        
        return [children,html.P(str(trigger))]
    
    return app

if __name__ == '__main__':

    app = create_app()
    app.run_server(debug=True)
