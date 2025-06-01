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