if (!window.dash_clientside) {
    window.dash_clientside = {}
}


window.dash_clientside.test_namespace = {
    test_function: function(chartType, data) {
        var categories = data.categories;
        var values1 = data.values1;
        var values2 = data.values2;

        var barmode = chartType === 'stack' ? 'stack' : 'group';

        return {
            'data': [
                {
                    'x': categories,
                    'y': values1,
                    'type': 'bar',
                    'name': 'Series 1'
                },
                {
                    'x': categories,
                    'y': values2,
                    'type': 'bar',
                    'name': 'Series 2'
                }
            ],
            'layout': {
                'title': `Bar Chart (${chartType === 'stack' ? 'Stacked' : 'Grouped'})`,
                'barmode': barmode
            }
        };
    }

};

// window.dash_clientside.clientside3 = {
//     update_table: function(clickdata, selecteddata, table_data, selectedrows, store) {
// 	/**
// 	 * Update selected rows in table when clicking or selecting in map
// 	 * chart
// 	 *
// 	 * Parameters
// 	 * ----------
// 	 *
// 	 * clickdata: object (dict)
// 	 *     clicked points
// 	 * selected: object (dict)
// 	 *     box-selected points
// 	 * table_data: list of dict
// 	 *     data of the table
// 	 * selectedrows: list of indices
// 	 *     list of selected countries to be updated
// 	 * store: list
// 	 *     store[1] is the list of countries to be used when initializing
// 	 *     the app
// 	 */
//     	if ((!selecteddata) && (!clickdata)) {
// 	    // this is only visited when initializing the app
// 	    // we use a pre-defined list of indices
// 	    return store[1];
//         }
// 	if (!selectedrows) {
// 	    selectedrows = [];
// 	}
// 	var ids = [...selectedrows];

// 	var countries = [];
// 	if (clickdata) {
// 	    var country = clickdata['points'][0]['customdata'][0];
// 	    countries.push(country);
// 	}
// 	if (selecteddata) {
// 	    var countries = [];
// 		for (i = 0; i < selecteddata['points'].length; i++) {
// 		    countries.push(selecteddata['points'][i]['customdata'][0]);
// 	    }
// 	}
// 	for (i = 0; i < countries.length; i++) {
// 	    for (j = 0; j < table_data.length; j++) {
// 		if (countries[i] == table_data[j]["country_region"]) {
// 		    if (selectedrows.includes(j)){
// 			var index = ids.indexOf(j);
// 			ids.splice(index, 1);
// 			}
// 		    else{
// 			ids.push(j);
// 		    }
// 		}
// 	    }
// 	}
// 	return ids;
//     }
// };
