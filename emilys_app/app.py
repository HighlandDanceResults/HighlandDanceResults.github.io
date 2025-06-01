# NOTES
# bootstrap-grid.css needed for card view
# 

from dash import Dash, dash_table, dcc, html, Input, Output, callback, State, clientside_callback
from dash.exceptions import PreventUpdate
import numpy as np
import pandas as pd
from collections import OrderedDict
import dash_bootstrap_components as dbc
from dash import html
import plotly.graph_objs as go
import plotly.express as px
import os
import dash_bootstrap_templates 

### --- CSV TO DF --- ###
data = pd.read_csv('/Users/ewood/Documents/GitHub/dance_website/emilys_app/data/test_all_new.csv', keep_default_na=False)
df = pd.DataFrame(data)
df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
df = df.replace('', np.NaN)



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='./assets')

DATA_TABLE_STYLE = {
    "style_data_conditional": [
        {"if": {"column_id": "Overall"}, "backgroundColor": "#e1eaf2"},
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#e1eaf2',
        },
        {
            'if': {'column_id': 'Name'},
            'textAlign': 'left'
        }
    ],
    "style_header": {
        "color": "black",
        "backgroundColor": "#799DBF",
        "fontWeight": "bold",
    }
}

### --- PAGE LAYOUT --- ###
navbar = html.Div(
    dbc.Card(
        dbc.CardHeader(
            html.Center([
                html.H3("Unofficial Highland Dance Results"),
                html.P("a passion project"),
            ])
        )
    ),style = {"margin-bottom": "0.3em"})

dropdown_labels = list(df['Year'].unique())

top_card = [
    dbc.CardHeader(html.B("Select Data")),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.P("1) Choose Year"),
                dcc.Dropdown(dropdown_labels, id= 'year_dropdown', searchable=False)
            ]),
            dbc.Col([
                html.P("2) Choose Competition"),
                dcc.Dropdown('', id= 'comp_dropdown', searchable=False)
            ]),
            dbc.Col([
                html.P("3) Choose Age Group"),
                dcc.Dropdown('', id= 'age_dropdown', searchable=False)
            ])
        ]),
        html.Br(),
        dbc.Row([
            html.Div([
                html.Button('Submit', id = 'submit-btn',
                            style = {"backgroundColor": "#e1eaf2"}
                ),
                html.Button('Reset Table', id = 'reset-btn',
                            style = {"backgroundColor": "#e1eaf2", "color":"red"}
                ),
            ], style={'textAlign': 'center'})
        ])
    ])
]

cards = dbc.Container(
    dbc.Col([
        dbc.Row(
            dbc.Card([
                dbc.CardHeader("Contact Us :)"),
                dbc.CardBody([
                    'Email with results, questions, or concerns at HighlandDanceResults@gmail.com'
                ],id = 'contact_card')
            ], style = {"padding": "0px", "margin-bottom": "0.5em"}) 
            
        ),
        dbc.Row(dbc.Card(top_card, style= {"padding": "0px"})
                , style = {"margin-bottom": "0.5em"}),
        dbc.Row(
            dbc.Card([
                dbc.CardHeader(html.B("Results")),
                dbc.CardBody([
                    'Please select data first...',
                    # dbc.Row(table_card),
                    # dbc.Row(plot_card)
                    dcc.Graph(id = 'test_graph')
                ],id = 'table_card')
            ], style= {"padding": "0px", "margin-bottom": "0.5em"})
        ),

    ])
, fluid=True, style= {"height": "80vh"})
                
app.layout = html.Div([
    dcc.Store(id='df_store', data=df.to_dict('records')),
    # dcc.Store(id='df_current', data=[]),
    navbar,
    cards
])

### --- POPULATING DROP DOWNS --- ###
# create year dropdown
app.clientside_callback(
    """
    function(year, df) {
        if (!year || !df) return [];
        const comps = [...new Set(df.filter(row => row.Year == year).map(row => row.Competition))];
        return comps.map(comp => ({ label: comp, value: comp }));
    }
    """,
    Output('comp_dropdown', 'options', allow_duplicate=True),
    Input('year_dropdown', 'value'),
    State('df_store', 'data'),
    prevent_initial_call=True
)
# create comp dropdown
app.clientside_callback(
    """
    function(comp, year, df) {
        if (!comp || !year || !df) return [];
        const ages = [...new Set(df.filter(row => row.Year == year && row.Competition == comp).map(row => row["Age Group"]))];
        return ages.map(age => ({ label: age, value: age }));
    }
    """,
    Output('age_dropdown', 'options', allow_duplicate=True),
    Input('comp_dropdown', 'value'),
    State('year_dropdown', 'value'),
    State('df_store', 'data'),
    prevent_initial_call=True
)


### --- POPULATING TABLE --- ###
app.clientside_callback(
    """
    function(n_clicks, year, comp, age, df) {

        const df_new = [df.filter(row => row.Year == year && row.Competition == comp && row["Age Group"])];

        return df_new;

    
    }
    """,
    Output('table_card', 'children', allow_duplicate=True),
    Input('submit-btn', 'n_clicks'),
    State('year_dropdown', 'value'),
    State('comp_dropdown', 'value'),
    State('age_dropdown', 'value'),
    State('df_store', 'data'),
    prevent_initial_call=True
)

# @app.callback(
#     Output('table_card', 'children', allow_duplicate=True),
#     # Output('df_chosen', 'data'),
#     Input('submit-btn', 'n_clicks'),
#     State('year_dropdown', 'value'),
#     State('comp_dropdown', 'value'),
#     State('age_dropdown', 'value'),
#     State('df_store', 'data'),
#     prevent_initial_call=True
# )
# def update_table(n_clicks, year_chosen, comp_chosen, age_chosen, df):
#     print(year_chosen)
#     print(comp_chosen)
#     print(age_chosen)
#     print(df)
#     return [year_chosen, comp_chosen, age_chosen, df]





# Serverside callback
# @app.callback(
#     Output('table_card', 'children', allow_duplicate=True),
#     Input('submit-btn', 'n_clicks'),
#     prevent_initial_call=True
# )
# def update_store_data(n_clicks):
#     if n_clicks == 'None' or n_clicks == 0:
#         PreventUpdate
#     print('nclicks: ', n_clicks)
#     # dff = df[df['Shipping Mode'] == shipping]
#     stored_figure = go.Figure(data = px.scatter(np.random.rand(30), np.random.rand(30)))
#     # store histogram on client side - browser
#     dcc.Tabs(id="tabs", value='tab_overall', children=[
#             dcc.Tab(label='Overall Results', value='tab_overall', children = dcc.Graph(figure=stored_figure)),
#         ])
#     return [stored_figure]


# app.clientside_callback(
#     """
#     function(figure_data, title_text) {
#         if(figure_data === undefined) {
#             return {'data': [], 'layout': {}};
#         }
#         const fig = Object.assign({}, figure_data, {
#                 'layout': {
#                     ...figure_data.layout,
#                     'title': {
#                         ...figure_data.layout.title, text: title_text
#                     }
#                 }
#         });
#         return fig;
#     }
#     """,
#     Output('clientside-graph', 'figure'),
#     Input('clientside-store-figure', 'data'),
#     Input('clientside-graph-title','value')
# )






if __name__ == '__main__':
    app.run(debug=False)
