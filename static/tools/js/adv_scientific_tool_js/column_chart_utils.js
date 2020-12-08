function create_query_json_column() {
    var sel_model = $('#model_name');
    var sel_scenario = $('#scenario_name');
    var sel_variable = $('#variable_name');

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
            "grouping": {"params":[], "aggregated_params":[]},
        },
        "additional_app_parameters": {
            "multiple_field": multiple_field,
            "val_list": val_list,
            "title_list": title_list
        }

    };

    //Retrieve units
   return retrieve_series_info_column(models, scenarios, variables, multiple_field, query_data);

}


function retrieve_series_info_column(models, scenarios, variables, multiple_field,query_data){
    const units_info = {
        "model_name": models,
        "scenario_name": scenarios,
        "variable_name": variables,
        "multiple": multiple_field   //gia pollaplh variable
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
            console.log(data);
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

function create_visualisation_col(query_id) {
            var viz_frame = $('#viz_iframe');
            viz_frame.off();
            viz_frame.hide();
            $('#loading_bar').show();
            var col_ordering_grouping = $('#col_order option:selected').attr('data-category');
            if ((col_ordering_grouping === "") && (col_ordering_grouping === null) && (col_ordering_grouping === undefined)) {
                col_ordering_grouping = "";
            }
            var data = {

                "row_categorisation_dataset": "datasetvariableharmonisationguides",
                "col_categorisation_dataset": col_ordering_grouping,
                "col_order": $('#col_order').val(),
                "row_order": "order",
                "y_var_names": ["var"],
                "y_axis_title": "Variables",
                "y_var_units": ["-"],
                "x_axis_name": "model",
                "x_axis_title": "Models",
                "x_axis_unit": "-",
                "z_axis_name": "status",
                "z_axis_title": "Value",
                "z_axis_unit": "-",
                "min_max_z_value": 0,
                "color_list_request": ["grey_green", "light_blue", "ice_gray"],
                "distinct": ["Extractable model output", "Harmonisable model input", "No explicit output or input"],
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

            console.log(url);
            var complete_url = "/visualiser/show_column_chart?" + url;
            viz_frame.attr('src', complete_url);
            viz_frame.on('load',function () {
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
                $(this).contents().on('click', function () {
                    console.log('select model & var');
                    var col_option = $('iframe').contents().find('#col_clicked').text();
                    var col_val = $('#model_name option')
                        .filter(function () {
                            return $.trim($(this).text()) === col_option;
                        }).val();
                    $('#model_name').val(col_val);
                    $('#model_name').trigger('change');
                    var row_option = $('iframe').contents().find('#row_clicked').text();
                    var row_val = $('#var_name option')
                        .filter(function () {
                            return $.trim($(this).text()) === row_option;
                        }).val();
                    $('#var_name').val(row_val);
                    $('#var_name').trigger('change');
                })
            });

        }