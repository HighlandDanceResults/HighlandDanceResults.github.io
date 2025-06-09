import dash_bootstrap_components as dbc
from dash import Dash, dash_table, dcc, html
from app_defs import table_style_data_conditional
import plotly.graph_objs as go
import pandas as pd

data = pd.read_csv('./data/data.csv', keep_default_na=False)

year_dropdown_labels = sorted(list(data['Year'].unique()))
name_dropdown_labels = sorted(list(data['Name'].unique()))

DATA_TABLE_STYLE = {
    "style_data_conditional": table_style_data_conditional(dcc.Store(id='df_chosen', data=[])),
    "style_header": {
        "color": "black",
        "backgroundColor": "#E6E6E6",
        "fontWeight": "bold",
    }
}

### --- PAGE LAYOUT --- ###
navbar = html.Div(
    dbc.Card([
        dbc.CardHeader(
            html.Center(dcc.Markdown('''# Unofficial Highland Dance Results'''))
        ),
    ]),style = {"margin-bottom": "0.3em"})


info_card = dbc.Card([
    dbc.CardHeader([
        html.B('Info')
    ]),
    dbc.CardBody([
        dcc.Markdown('''            
            Checkout [scotdance.app] (https://scotdance.app/#/competitions/), which also has a mobile app! This website originated because some comps do not use the app.
            ''')
    ]),
], style= {"padding": "0px"})

select_data_card = [html.B("Select Tab"),
            dbc.Tabs(
                [
                    dbc.Tab(label="Comp. Search", tab_id="comp_tab", label_style={"color": "#000000"}),
                    dbc.Tab(label="Dancer Search", tab_id="search_tab", label_style={"color": "#000000"}),
                ],
            id="tabs",
            active_tab="comp_tab"
        )]

dancer_search_card = [
    dbc.CardBody([
        dbc.Col([
            dbc.Row([
                dcc.Markdown('''
                    **Choose/Search Dancer Name**
                             
                    Select name from list or type in dancer name. Click on desired name.
                '''),
                dcc.Dropdown(name_dropdown_labels,
                            id= 'name_dropdown',
                            searchable=True,
                            optionHeight=50,
                            placeholder= 'Type in or Select Dancer Name'
                            )
            ]),
        ])
    ]),
]

competition_card = [
    dbc.CardBody([
        dbc.Col([
            dbc.Row([
                dcc.Markdown('''**1) Choose Year**'''),
                dcc.Dropdown(year_dropdown_labels,
                             id= 'year_dropdown',
                             searchable=False,
                             optionHeight=50,
                             placeholder= 'Select Year'
                             )

            ]),
        ])]),
    dbc.CardBody([
        dbc.Col([
            dbc.Row([
                dcc.Markdown('''**2) Choose Competition**'''),
                dcc.Dropdown('',
                             id= 'comp_dropdown',
                             searchable=False,
                             optionHeight=50,
                             style = {'white-space': 'nowrap', 'position': 'initial'},
                            placeholder= 'Select Competition'
                ),
            ]),
        ])]),
    dbc.CardBody([
        dbc.Col([
            dbc.Row([
                dcc.Markdown('''**3) Choose Age Group**'''),
                dcc.Dropdown('',
                             id= 'age_dropdown',
                             searchable=False,
                             optionHeight=50,
                            placeholder= 'Select Age Group'
                ),
            ])
        ]),
        dbc.Row([
            dbc.CardBody([
                dbc.Button('Submit', id = 'comp_submit_btn', outline=True, color = 'dark', className="me-1",
                            style = {"backgroundColor": "#e1eaf2"}
                ),
                dbc.Button('Reset', id = 'reset_btn', outline=True, color = 'dark', className="me-1",
                            style = {"backgroundColor": "#e1eaf2", "color":"red"}
                ),
            ], style={'textAlign': 'center'})
        ])
    ])
]

results_card =  dbc.Card([
                dbc.CardHeader(html.B("Results")),
                dbc.CardBody([
                    dcc.Markdown('''Please select year, competition, and age group first.''', id = 'data_markdown'),
                    html.Center([
                        dcc.Markdown('', id = 'table_title'),
                        dash_table.DataTable(id = 'table',
                            style_as_list_view=True,
                            sort_action = 'native',
                            style_data_conditional = DATA_TABLE_STYLE.get("style_data_conditional"),
                            style_header=DATA_TABLE_STYLE.get("style_header"),
                            style_cell = {'textAlign': 'center',
                                          'font-family':'sans-serif'},
                            style_table={'overflowX': 'auto',
                                'minWidth': '90vw', 'width': '90vw', 'maxWidth': '90vw'
                                        },
                            fixed_columns={'headers': True, 'data': 1},
                    )]),
                ]),
                dbc.CardBody([
                    html.Center(dcc.Markdown('', id = 'graph_title')),
                    dcc.Graph(id = 'graph',
                        figure={
                            'data': [],
                            'layout': go.Layout(                                
                                xaxis =  {'showgrid': False, 'zeroline': False, 'ticks':'', 'showticklabels':False},
                                yaxis = {'showgrid': False, 'zeroline': False, 'ticks':'', 'showticklabels':False}                                                               
                                )
                            })
                    # dbc.Row(table_card),
                    # dbc.Row(plot_card)
                ])
            ], style= {"padding": "0px", "margin-bottom": "0.5em"}
)

contact_card = dbc.Card([
    dbc.CardHeader("Contact Us"),
    dbc.CardBody([
        dcc.Markdown('''
            This is a passion project maintained by a single person in my free time. Please by nice :) 
                        
            Email with results or corrections at <highlanddanceresults@gmail.com>
                        ''')
        ],id = 'contact_card')
    ], style= {"padding": "0px", "margin-bottom": "0.5em"}
)
        

cards = dbc.Container(
    dbc.Col([
        dbc.Row(info_card, style = {"margin-bottom": "0.5em"}),
        dbc.Row([
            dbc.Card([
                dbc.CardHeader(
                    select_data_card
                ),
                dbc.CardBody(
                    competition_card, id = 'selected_tab_card'
                )
                # select_data_card, style= {"padding": "0px"}
            ], style= {"padding": "0px", "margin-bottom": "0.5em"})
            
        ]

        , style = {"margin-bottom": "0.5em"}),
        dbc.Row(results_card),
        dbc.Row(contact_card),
    ]), fluid=True,
        style = {'minWidth': '96vw',
                    'width': '96vw',
                    'maxWidth': '96vw',
                    'align-items': 'center',
                    "height": "80vh"}
    )