from dash import Dash, dash_table, dcc, html, Input, Output, callback, State, clientside_callback
# import dash
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

# Sample data (replace with actual file or source)
# data = {
#     'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
#     'Year': [2023, 2023, 2024, 2024],
#     'Competition': ['Highland Games', 'Highland Games', 'Celtic Fest', 'Celtic Fest'],
#     'Age Group': ['10-12', '10-12', '13-15', '13-15'],
#     'Overall': [1, 2, 1, 2],
#     'Fling': [1, 2, 1, 2],
#     'Sword': [1, 2, 1, 2],
#     'Reel': [1, 2, 1, 2]
# }
# df = pd.DataFrame(data)

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


data = pd.read_csv('/Users/ewood/Documents/GitHub/dance_website/emilys_app/data/test_all_new.csv', keep_default_na=False)
df = pd.DataFrame(data)
df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
df = df.replace('', np.NaN)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP,
                                 'assets/bootstrap-grid.css'],
            suppress_callback_exceptions=True
           )

app.layout = html.Div([
    dcc.Store(id='df_store', data=df.to_dict('records')),

    html.Div([
        html.Label('Year:'),
        dcc.Dropdown(id='year_dropdown', options=[{'label': y, 'value': y} for y in sorted(df['Year'].unique())]),

        html.Label('Competition:'),
        dcc.Dropdown(id='comp_dropdown'),

        html.Label('Age Group:'),
        dcc.Dropdown(id='age_dropdown'),

        html.Button('Submit', id='submit-btn'),
        html.Button('Reset', id='reset-btn')
    ]),

    html.Div(id='table_card', children=['Please select data first...'])
])

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

# Submit button triggers data filtering and plot
app.clientside_callback(
    """
    function(n_clicks, year, comp, age, df) {
        if (!n_clicks || !year || !comp || !age || !df) {
            return ["Please select options first..."];
        }

        const filtered = df.filter(row => row.Year == year && row.Competition == comp && row["Age Group"] == age);
        if (filtered.length === 0) return ["No data found"];

        const columns = Object.keys(filtered[0])
            .filter(col => !["Competition", "Year", "Age Group"].includes(col))
            .map(col => ({ name: col, id: col }));

        const table = {
            props: {
                id: 'df_chosen',
                data: filtered.map(row => {
                    const r = { ...row };
                    delete r["Year"];
                    delete r["Competition"];
                    delete r["Age Group"];
                    return r;
                }),
                columns: columns,
                sort_action: 'native',
                style_cell: { textAlign: 'center' },
                style_data_conditional: [
                    {
                        if: { column_id: 'Overall' },
                        backgroundColor: '#e1eaf2'
                    },
                    {
                        if: { row_index: 'odd' },
                        backgroundColor: '#e1eaf2'
                    },
                    {
                        if: { column_id: 'Name' },
                        textAlign: 'left'
                    }
                ],
                style_header: {
                    color: 'black',
                    backgroundColor: '#799DBF',
                    fontWeight: 'bold'
                }
            },
            type: 'DashDataTable'
        };

        const exclude = ['Competition', 'Year', 'Age Group', 'Number', 'Name', 'Overall'];
        const keys = Object.keys(filtered[0]).filter(k => !exclude.includes(k));
        const traces = filtered.map(row => ({
            type: 'scatter',
            mode: 'lines+markers',
            name: row.Name,
            x: keys,
            y: keys.map(k => row[k])
        }));

        const figure = {
            data: traces,
            layout: {
                title: { text: 'Placement Visualized', x: 0.5 },
                yaxis: { autorange: 'reversed' }
            }
        };

        const graph = {
            props: { figure: figure },
            type: 'Graph'
        };

        return [
            { type: 'P', props: { children: 'Results', style: { textAlign: 'center', fontSize: '18px' } } },
            { type: 'Div', props: { children: [table] } },
            { type: 'Div', props: { children: [graph] } }
        ];
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

# Reset button
app.clientside_callback(
    """
    function(n) {
        return ['Please select data first...'];
    }
    """,
    Output('table_card', 'children', allow_duplicate=True),
    Input('reset-btn', 'n_clicks'),
    prevent_initial_call=True
)

if __name__ == '__main__':
    app.run_server(debug=False)
