def table_style_data_conditional(df_chosen):
    styles = [
        {"if": {"column_id": "Overall"}, "backgroundColor": "#f9f9f9"},
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': "#f9f9f9",
        },
        {
            'if': {'column_id': 'Name'},
            'textAlign': 'left'
        }
    ]
    return styles

