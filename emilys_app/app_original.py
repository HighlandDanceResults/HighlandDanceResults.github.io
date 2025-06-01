# NOTES
# bootstrap-grid.css needed for card view
# 

from dash import Dash, dash_table, dcc, html, Input, Output, callback
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

data = pd.read_csv('/Users/ewood/Documents/GitHub/dance_website/emilys_app/data/test.csv', keep_default_na=False)
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

dropdown_labels = []
for file in os.listdir('/Users/ewood/Documents/GitHub/dance_website/emilys_app/data'):
    dropdown_labels.append(file)

top_card = [
    dbc.CardHeader(html.B("Test Header")),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.P("1) Choose Competition"),
                dcc.Dropdown(dropdown_labels, id= 'comp_dropdown', searchable=False)
            ]),
            dbc.Col([
                html.P("2) Choose Age Group"),
                dcc.Dropdown(dropdown_labels, id= 'age_dropdown', searchable=False)
            ])
        ])
    ])
]

table_card = [
        dash_table.DataTable(
            id = 'main_table',
            data = df.to_dict('records'),
            sort_action = 'custom',
            columns=[{'name': column, 'id':column} for i, column in enumerate(df.columns)],
            style_data_conditional = DATA_TABLE_STYLE.get("style_data_conditional"),
            style_header=DATA_TABLE_STYLE.get("style_header"),
            style_cell = {'textAlign': 'center'},
        )
]

navbar = html.Div(dbc.Card(dbc.CardHeader(html.Center(html.H1("United States Highland Dance Results")))),
                  style = {"margin-bottom": "0.3em"})

y = df[['Fling', 'Sword', 'Seann Truibhas', 'Reel']].values
x = ['Fling', 'Sword', 'Seann Truibhas', 'Reel']

fig = go.Figure(
    data=[go.Scatter(x = x, y = yi, name = df['Name'].iloc[i]) for i,yi in enumerate(y)]
    )

fig.update_yaxes(autorange = "reversed")
fig.update_layout(title_text='Results Over Time', title_x=0.5)


plot_card = [
        dcc.Graph(figure=fig)
]

cards = dbc.Container(
    dbc.Col([
        dbc.Row(dbc.Card(top_card, style= {"padding": "0px"})
                , style = {"margin-bottom": "0.5em"}),
        dbc.Row(
            dbc.Card([
                dbc.CardHeader("Results"),
                dbc.CardBody([
                    dbc.Row(table_card),
                    dbc.Row(plot_card)
                ])
            ], style= {"padding": "0px"})
        )
    ])
, fluid=True, style= {"height": "80vh"})
                


app.layout = html.Div([navbar, cards])

# app.layout = dash_table.DataTable(
#     id = 'main_table',
#     data = df.to_dict('records'),
#     sort_action = 'custom',
#     columns=[{'name': column, 'id':column} for i, column in enumerate(df.columns)],
#     style_data_conditional = DATA_TABLE_STYLE.get("style_data_conditional"),
#     style_header=DATA_TABLE_STYLE.get("style_header")
# )

@app.callback(
    Output('main_table', 'data'),
    Input('main_table', 'sort_by')
)
def sorting(sort):
    if sort is None :
        raise PreventUpdate
    else :
        dff = df.sort_values(
            by = [s['column_id'] for s in sort],
            ascending = [True if s['direction']=='asc' else False for s in sort],
            inplace=False,
            na_position= 'last'
        )
        
    return dff.to_dict('records')

    # style_data_conditional=[
    #     {
    #         'if': {
    #             'column_id': 'Region',
    #         },
    #         'backgroundColor': 'dodgerblue',
    #         'color': 'white'
    #     },
    #     {
    #         'if': {
    #             'filter_query': '{Humidity} > 19 && {Humidity} < 41',
    #             'column_id': 'Humidity'
    #         },
    #         'backgroundColor': 'tomato',
    #         'color': 'white'
    #     },

    #     {
    #         'if': {
    #             'column_id': 'Pressure',

    #             # since using .format, escape { with {{
    #             'filter_query': '{{Pressure}} = {}'.format(df['Pressure'].max())
    #         },
    #         'backgroundColor': '#85144b',
    #         'color': 'white'
    #     },

    #     {
    #         'if': {
    #             'row_index': 5,  # number | 'odd' | 'even'
    #             'column_id': 'Region'
    #         },
    #         'backgroundColor': 'hotpink',
    #         'color': 'white'
    #     },

    #     {
    #         'if': {
    #             'filter_query': '{id} = 4',  # matching rows of a hidden column with the id, `id`
    #             'column_id': 'Region'
    #         },
    #         'backgroundColor': 'RebeccaPurple'
    #     },

    #     {
    #         'if': {
    #             'filter_query': '{Delivery} > {Date}', # comparing columns to each other
    #             'column_id': 'Delivery'
    #         },
    #         'backgroundColor': '#3D9970'
    #     },

    #     {
    #         'if': {
    #             'column_editable': False  # True | False
    #         },
    #         'backgroundColor': 'rgb(240, 240, 240)',
    #         'cursor': 'not-allowed'
    #     },

    #     {
    #         'if': {
    #             'column_type': 'text'  # 'text' | 'any' | 'datetime' | 'numeric'
    #         },
    #         'textAlign': 'left'
    #     },

    #     {
    #         'if': {
    #             'state': 'active'  # 'active' | 'selected'
    #         },
    #        'backgroundColor': 'rgba(0, 116, 217, 0.3)',
    #        'border': '1px solid rgb(0, 116, 217)'
    #     }

    # ]
# )

if __name__ == '__main__':
    app.run(debug=False)
