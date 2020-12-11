function create_query_json_column() {
    var sel_model = $('#model_name_intro_comp');
    var sel_scenario = $('#scenario_name_intro_comp');
    var sel_variable = $('#variable_name_intro_comp');

    const models = sel_model.multipleSelect('getSelects');
    const scenarios = sel_scenario.multipleSelect('getSelects');
    const variables = sel_variable.multipleSelect('getSelects');

    var multiple_field = "model";
    var val_list = models;
    var title_list = sel_model.multipleSelect('getSelects', 'text');

    $('select.boot-select').each(function () {
        if ($(this).multipleSelect('getSelects').length > 1) {
            multiple_field = $(this).data('dbname');
            val_list = $(this).multipleSelect('getSelects');
            title_list = $(this).multipleSelect('getSelects', 'text');
        }
    });
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
    selected.push('value', 'year');
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
                    "parameter": "year",
                    "ascending": true
                },
            ]
            ,
            "grouping": {"params":["year"], "aggregated_params":[]},
        },
        "additional_app_parameters": {
            "multiple_field": multiple_field,
            "val_list": val_list,
            "title_list": title_list
        }

    };

    //Retrieve units
    console.log("query data=", query_data)
   return retrieve_series_info_column(models, scenarios, variables, multiple_field, query_data);

}


function retrieve_series_info_column(models, scenarios, variables, multiple_field,query_data){
    const units_info = {
        "model_name": models,
        "scenario_name": scenarios,
        "variable_name": variables,
        "multiple": multiple_field   //gia pollaplh variable
    };
    console.log("units info=", units_info);
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
            console.log("check instances=", data);
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

    return {
        "data": query_data,
        "multiple_field": multiple_field,
        "val_list": final_val_list,
        "title_list": final_title_list,
        "unit_list": final_unit_list
    };

}

function create_visualisation_col(query_id, val_list, title_list, unit_list, variable) {
    var viz_frame = $('#viz_iframe_intro_comp');
    console.log("val list=", val_list);
    console.log("title list=", title_list);
    console.log("unit list=", unit_list);
    console.log("variable", variable);

    viz_frame.off();
    viz_frame.hide();
    $('#loading_bar').show();

    //http://localhost:8000/visualiser/show_column_chart?
    // y_var_names[]=CP_ContEmissionIntensity&
    // y_var_names[]=CP_GDPPerCapita&
    // y_var_names[]=NDC_GDPPerCApita&
    //
    // y_var_titles[]=CP_ContEmissionIntensity&
    // y_var_titles[]=CP_GDPPerCapita&y_var_titles[]=NDC_GDPPerCApita&

    // y_var_units[]=people&
    // y_var_units[]=people&
    //
    // x_axis_type=text&
    // x_axis_name=year&
    // x_axis_title=Year&y_axis_title=Population&color_list_request[]=blue&
    //
    // color_list_request[]=red&
    // color_list_request[]=green&
    // use_default_colors=false&
    //
    // chart_3d=true&use_default_colors=false&dataset=250&dataset_type=query
    var data = {
        "y_var_names": val_list,
        "y_var_titles": title_list,
        "y_var_units": unit_list,
        "y_axis_title": String(variable),
        "x_axis_name": "year",
        "x_axis_title": "Year",
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

    console.log("complete url=", url)
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
                console.log(data);
            }
        });

        $('#loading_bar').hide();

    });

}