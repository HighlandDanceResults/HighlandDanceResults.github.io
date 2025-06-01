# NOTES
# bootstrap-grid.css needed for card view
# 

from dash import Dash, dash_table, dcc, html, Input, Output, callback, State
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

data = pd.read_csv('./data/test_all_new.csv', keep_default_na=False)
df = pd.DataFrame(data)
df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
df = df.replace('', np.NaN)



app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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
navbar = html.Div(dbc.Card(dbc.CardHeader(html.Center(html.H1("Unofficial Highland Dance Results")))),
                  style = {"margin-bottom": "0.3em"})


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
        dbc.Row(dbc.Card(top_card, style= {"padding": "0px"})
                , style = {"margin-bottom": "0.5em"}),
        dbc.Row(
            dbc.Card([
                dbc.CardHeader("Results"),
                dbc.CardBody([
                    'Please select options first...'
                    # dbc.Row(table_card),
                    # dbc.Row(plot_card)
                ],id = 'table_card')
            ], style= {"padding": "0px", "margin-bottom": "0.5em"})
        ),
        dbc.Row(
            dbc.Card([
                dbc.CardHeader("Contact Us :)"),
                dbc.CardBody([
                    'Email us with results, questions, or concerns at highlanddanceresults@gmail.com'
                ],id = 'contact_card')
            ], style = {"margin-bottom": "0.5em"})
            
        )
    ])
, fluid=True, style= {"height": "80vh"})
                


app.layout = html.Div([
    dcc.Store(id='df_store', data=df.to_dict('records')),
    navbar,
    cards
])

### --- POPULATING DROP DOWNS --- ###
# Populate Competition based on Year
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

# Populate Age Group based on Competition and Year
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





# # App layout
# app.layout = html.Div([
#     dcc.Graph(id='bar-chart'),
#     dcc.Dropdown(
#         id='chart-type-dropdown',
#         options=[
#             {'label': 'Grouped', 'value': 'group'},
#             {'label': 'Stacked', 'value': 'stack'}
#         ],
#         value='group',  # Default value
#         clearable=False,
#         style={'width': '50%'}
#     ),
#     dcc.Store(id='bar-data', data={'categories': categories, 'values1': list(values1), 'values2': list(values2)})
# ])

# Client-side callback (JavaScript function)
# app.clientside_callback(
#     """
#     function(chartType, data) {
#         var categories = data.categories;
#         var values1 = data.values1;
#         var values2 = data.values2;

#         var barmode = chartType === 'stack' ? 'stack' : 'group';

#         return {
#             'data': [
#                 {
#                     'x': categories,
#                     'y': values1,
#                     'type': 'bar',
#                     'name': 'Series 1'
#                 },
#                 {
#                     'x': categories,
#                     'y': values2,
#                     'type': 'bar',
#                     'name': 'Series 2'
#                 }
#             ],
#             'layout': {
#                 'title': `Bar Chart (${chartType === 'stack' ? 'Stacked' : 'Grouped'})`,
#                 'barmode': barmode
#             }
#         };
#     }
#     """,
#     Output('bar-chart', 'figure'),
#     [Input('chart-type-dropdown', 'value')],
#     [Input('bar-data', 'data')]
# )

# app.clientside_callback(
#     ClientsideFunction(
#         namespace='test_namespace',
#         function_name='test_function'
#     ),
#     output=Output('bar-chart', 'figure'),
#     inputs=[
#         Input('chart-type-dropdown', 'value'),
#         Input('bar-data', 'data')
#     ]
# )

# app.clientside_callback(
#     ClientsideFunction(
#         namespace='clientside3',
#         function_name='update_table'
#     ),
#     output=Output('table', 'selected_rows'),
#     inputs=[
#         Input('map', 'clickData'),
#         Input('map', 'selectedData'),
#         Input('table', 'data')
#         ],
#     state=[State('table', 'selected_rows'),
#            State('store', 'data')],
#     )



# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)