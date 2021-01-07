function create_query_json_column() {
    var sel_model = $('#model_name_intro_comp');
    var sel_scenario = $('#scenario_name_intro_comp');
    var sel_variable = $('#variable_name_intro_comp');

    const models = new Array(1);
    models[0] = sel_model.val();

    const scenarios = sel_scenario.val();

    const variables = new Array(1);
    variables[0] = sel_variable.val();

    console.log("models are:", models);
    console.log("scenarios are:", scenarios);
    console.log("variables are:", variables);

    var aggfunc = $('#agg_func_intro_comp');
	var aggvar = $('#agg_var_intro_comp');

	const aggfuncval = new Array(1);
	aggfuncval[0] = aggfunc.val();

	const aggvarval =  new Array(1);
	aggvarval[0] = aggvar.val();


	var e = document.getElementById("agg_var_intro_comp");
	const aggvartitle = new Array(1);
	aggvartitle[0] = e.options[e.selectedIndex].text;;

	console.log("aggfunc=", aggfuncval);
	console.log("aggvar=", aggvarval);
	console.log("aggvartitle=", aggvartitle);

    var multiple_field = "scenario";
    var val_list = scenarios;
    var title_list = sel_scenario.multipleSelect('getSelects', 'text');


    // $('select.boot-select').each(function () {
    //     if ($(this).multipleSelect('getSelects').length > 1) {
    //         multiple_field = $(this).data('dbname');
    //         val_list = $(this).multipleSelect('getSelects');
    //         title_list = $(this).multipleSelect('getSelects', 'text');
    //     }
    // });
    if(val_list.length===0){
        val_list = []
    }

    const input_dict = {'model__name': models, 'scenario__name': scenarios, 'variable__name': variables};
    var selected = [];
    for (var i in input_dict) {
        if (input_dict[i].length > 0) {
            selected.push(i);
        }
    }
    var and_dict = [];
    var or_dict = [];
    for (var j in selected) {
        var temp = input_dict[selected[j]];
        if (temp.length > 1) {
            for (var x in temp) {
                or_dict.push({
                    'operand_1': selected[j],
                    'operand_2': temp[x],
                    'operation': '='
                });
            }
        } else {
            and_dict.push({
                'operand_1': selected[j],
                'operand_2': input_dict[selected[j]][0],
                'operation': '='
            });
        }
    }
    console.log('new1'+ selected);
    selected.push('value', 'year');
    console.log('new2' + selected);
    const query_data = {
        "dataset": "i2amparis_main_resultscomp",
        "query_configuration": {
            "select": selected,
            "filter": {
                "and": and_dict,
                "or": or_dict
            },
            "ordering": [
                {
                    "parameter": aggvarval[0],
                    "ascending": true
                },
            ]
            ,
            "grouping": {"params":[aggvarval[0], "model__name", "scenario__name", "variable__name"], "aggregated_params":[{"name":"value","agg_func": aggfuncval[0]}]},
        },
        "additional_app_parameters": {
            "multiple_field": multiple_field,
            "val_list": val_list,
            "title_list": title_list,
            "grouping_var": aggvarval[0],
            "grouping_var_title": aggvartitle[0]
        }

    };
    console.log(query_data);

    //Retrieve units
   return retrieve_series_info_column(models, scenarios, variables, multiple_field, query_data);

}


function retrieve_series_info_column(models, scenarios, variables, multiple_field,query_data){
    const units_info = {
        "model_name": models,
        "scenario_name": scenarios,
        "variable_name": variables,
        "multiple": multiple_field,
    };

    var instances = [];
    var final_val_list = [];
    var final_title_list = [];
    var final_unit_list = [];
    $.ajax({
        url: "/data_manager/retrieve_series_info",
        type: "POST",
        data: JSON.stringify(units_info),
        contentType: 'application/json',
        success: function (data) {

            instances = data["instances"];
            for (var i = 0; i < instances.length; i++) {
                final_val_list.push(instances[i]['series']);
                final_title_list.push(instances[i]['title']);
                final_unit_list.push(instances[i]['unit']);
            }

        },
        error: function (data) {
            console.log(data);
        }
    });
    var grouping_val;
    var grouping_var_title;
    if('grouping_var' in query_data['additional_app_parameters']){
        grouping_val = query_data['additional_app_parameters']['grouping_var']//the variable that is used for the column grouping
        grouping_var_title = query_data['additional_app_parameters']['grouping_var_title']//the title of the variable that is used for the column grouping
    }else{
        grouping_val = ''
    }

    return {
        "data": query_data,
        "multiple_field": multiple_field,
        "val_list": final_val_list,
        "title_list": final_title_list,
        "unit_list": final_unit_list,
        "grouping_var": grouping_val,
        "grouping_var_title": grouping_var_title
    };

}

function create_visualisation_col(query_id, val_list, title_list, unit_list, grouping_val, grouping_var_title, variable) {
    var viz_frame = $('#viz_iframe_intro_comp');
    viz_frame.off();
    viz_frame.hide();
    $('#loading_bar').show();


    var data = {
        "y_var_names": val_list,
        "y_var_titles": title_list,
        "y_var_units": unit_list,
        "y_axis_title": String(variable),
        "x_axis_name": grouping_val,
        "x_axis_title":grouping_var_title,
        "x_axis_unit": "-",
        "x_axis_type": "text",
        "color_list_request": ["moody_blue", "dark_blue", "violet", "light_red", "ceramic", "orange_yellow", "grey_green", "cyan", "black"],
        "dataset": query_id,
        "dataset_type": "query",
    };
    var url = '';
    for (var key in data) {
        if (data.hasOwnProperty(key)) {
            if (Array.isArray(data[key])) {
                for (var j = 0; j < data[key].length; j++) {
                    url = url + String(key) + '[]' + "=" + String(data[key][j]) + '&'
                }
            } else {
                url = url + String(key) + "=" + String(data[key]) + '&'
            }

        }
    }

    var complete_url = "/visualiser/show_column_chart?" + url;
    viz_frame.attr('src', complete_url);
    viz_frame.on('load', function () {
        $(this).show();
        console.log("delete old query");
        $.ajax({
            url: "/data_manager/delete_query",
            type: "POST",
            data: JSON.stringify(query_id),
            contentType: 'application/json',
            success: function (data) {
                console.log(data);
            },
            error: function (data) {
            }
        });

        $('#loading_bar').hide();

    });

}

const capitalize = (s) => {
    if (typeof s !== 'string') return ''
    return s.charAt(0).toUpperCase() + s.slice(1)
}