# NOTES
# bootstrap-grid.css needed for card view
# test

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
from app_layout import navbar, cards, competition_card

data = pd.read_csv('./data/data.csv', keep_default_na=False)
df = pd.DataFrame(data)
df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
df = df.replace('', np.NaN)

year_dropdown_labels = list(df['Year'].unique())
name_dropdown_labels = list(df['Name'].unique())


app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           assets_folder='/Users/ewood/Documents/GitHub/HighlandDanceResults.github.io/assets/',
           title="Highland Dance Results",
           prevent_initial_callbacks=True)

                
app.layout = html.Div([
    dcc.Store(id='df_store', data=df.to_dict('records')),
    dcc.Store(id='df_chosen', data=[]),
    dcc.Store(id='competition_cards_store', data=competition_card),
    # dcc.Store(id='dancer_search_card_store', data=dancer_search_card),
    navbar,
    cards
])

### --- POPULATING DROP DOWNS --- ###
# app.clientside_callback(
#     """
#     function(active_tab, competition_cards_store, dancer_search_card_store) {
#         if (active_tab == 'comp_tab'){
#             return competition_cards_store;
#         } 
#         if (active_tab == 'search_tab'){
#             return dancer_search_card_store;
#         }
#     }
#     """,
#     Output("selected_tab_card", "children"),
#     [Input("tabs", "active_tab"),
#     State("competition_cards_store", "data"),
#     State("dancer_search_card_store", "data")
#     ]
# )
# @app.callback(
#         Output("selected_tab_card", "children"),
#         [Input("tabs", "active_tab"),
#          State("competition_cards_store", "data"),
#          State("dancer_search_card_store", "data")
#          ])
# def tab_content(active_tab, competition_cards_store, dancer_search_card_store):
#     if active_tab == 'comp_tab':
#         return competition_cards_store
#     elif active_tab == 'search_tab':
#         return dancer_search_card_store

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


# table card
app.clientside_callback(
    """
    function(n_clicks, year, comp, age, df) {
        if (n_clicks < 1) return [];

        const drop_list = ["Competition", "Year", "Age Group", "Number"];
        const drop_list_for_table = ["Competition", "Year", "Age Group"];

        const df_chosen = df.filter(row => row.Year == year && row.Competition == comp && row["Age Group"] == age);

        var dance_to_placings = df_chosen.map(function(row) {
            const newRow = {};
            for (const key in row) {
                if (!drop_list.includes(key)) {
                    newRow[key] = row[key];
                }
            }
            return newRow;
        });

        var table_data = df_chosen.map(function(row) {
            const newRow = {};
            for (const key in row) {
                if (!drop_list_for_table.includes(key)) {
                    newRow[key] = row[key];
                }
            }
            return newRow;
        });

        const chosen_dances = Array.from(new Set(dance_to_placings.flatMap(obj => Object.keys(obj))));
        const placings = dance_to_placings.map(obj => chosen_dances.map(key => obj[key]));

        var figure_data = [];
        for (let i = 0; i < df_chosen.length; i++) {
            figure_data.push(
                {'name': placings[i][0],
                'x': chosen_dances.slice(1),
                'y': placings[i].slice(1),
                'marker': {'symbol':'cirlce',
                    'size':12},
                'type': 'scatter'}
            );

        };

        const graph_data = {
            'data': figure_data,
            'layout': {
                'yaxis': {autorange: 'reversed',
                    'side':'left',
                    'fixedrange':true},
                'xaxis': {'side': 'top',
                    'fixedrange':true},
                'legend': {'orientation': 'h',
                    'y':0,
                    'yanchor': "bottom",
                    'yref': "container"},
                'margin': {l:15, r:0, t:0},
                'hovermode':'x',
                //'title' : {'text':'Results for Dancers For Each Dance'}
            }
        };

        var selected_data = 'Results for ' + year + ' '+ comp + ' ' +age+':';

        tips = `  
            **Viewing Tips:**     
            * Turn phone sideways
            * Table Tip - Scroll left/right
            * Table Tip - Sort by clicking up/down arrows on column titles
            * Graph Tip - Click on graph points for more info
            * Graph Tip - Double click on dancer name in legend to view individual results
            `

        var table_title = '**'+ 'Table ' + selected_data +'**'
        var graph_title = '**'+ 'Plotted ' + selected_data +'**'
        
        return [graph_data,
            table_data,
            df_chosen,
            tips,
            table_title,
            graph_title];
    }
    """,
    Output('graph', 'figure', allow_duplicate=True),
    Output('table', 'data', allow_duplicate=True),
    Output('df_chosen', 'data', allow_duplicate=True),
    Output('data_markdown', 'children', allow_duplicate=True),
    Output('table_title', 'children'),
    Output('graph_title', 'children'),

    Input('comp_submit_btn', 'n_clicks'),
    State('year_dropdown', 'value'),
    State('comp_dropdown', 'value'),
    State('age_dropdown', 'value'),
    State('df_store', 'data'),
    prevent_initial_call=True
)


# resetting graph and table
app.clientside_callback(
    """
    function(n_clicks) {

        const empty_graph = {
            'data': [],
            'layout': {'xaxis': {'showgrid': false,
                'showticklabels': false,
                'ticks': '',
                'zeroline': false},
                'yaxis': {'showgrid': false,
                'showticklabels': false,
                'ticks': '',
                'zeroline': false}}};

        return [[], empty_graph, [], [], [], [], [], []];
    }
    """,
    Output('table', 'data', allow_duplicate=True),
    Output('graph', 'figure', allow_duplicate=True),
    Output('data_markdown', 'children', allow_duplicate=True),
    Output('year_dropdown', 'value', allow_duplicate=True),
    Output('comp_dropdown', 'value', allow_duplicate=True),
    Output('age_dropdown', 'value', allow_duplicate=True),
    Output('table_title', 'children', allow_duplicate=True),
    Output('graph_title', 'children', allow_duplicate=True),

    Input('reset_btn', 'n_clicks'),
    prevent_initial_call=True
)


# Run the app
if __name__ == '__main__':
    app.run(debug=False)