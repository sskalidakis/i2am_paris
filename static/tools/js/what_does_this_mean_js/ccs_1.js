$(document).ready(function () {

    var viz_frame_ccs = $('#ccs_viz_iframe');

    viz_frame_ccs.show();
    /* Token Retrieval*/
    const csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    });

    /* # Query creation*/
    var jq_obj_ccs = create_query(['Carbon Sequestration|CCS'], ['PR_CurPol_CP', 'PR_CurPol_EI', '', 'PR_NDC_EI', 'PR_NDC_CP'],
        ['World'], ['42', 'e3me', 'gcam', 'gemini_e3', 'ices', 'muse', 'tiam'], 2000, 2050, []);
    retrieve_series_info_global_ccs_1(jq_obj_ccs);


    function start_qc_v_global_ccs_1_process(json_query_obj, variable) {
        var query = {};
        query["query_name"] = "wdtm_ccs_query";
        query["parameters"] = json_query_obj['data'];
        // var variable_selection = (variable_sel.multipleSelect('getSelects', 'text'));
        $.ajax({
            url: "/data_manager/create_query",
            type: "POST",
            data: JSON.stringify(query),
            contentType: 'application/json',
            success: function (data) {
                console.log('Global CCS Query Saved in DB');
                var query_id = data['query_id'];
                create_visualisation_global_ccs_1(query_id, json_query_obj['val_list'], json_query_obj['title_list'], json_query_obj['unit_list'], variable);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }


    function create_visualisation_global_ccs_1(query_id, val_list, title_list, unit_list, variable) {
        var viz_frame = $('#ccs_viz_iframe');
        viz_frame.off();
        viz_frame.hide();
        $('#ccs_loading_bar').show();

        var data = {
            "y_var_names": val_list,
            "y_var_titles": title_list,
            "y_var_units": unit_list,
            "y_axis_title": 'Global ' + String(variable[0]),
            "x_axis_name": "year",
            "x_axis_title": "Year",
            "x_axis_unit": "-",
            "x_axis_type": "text",
            "color_list_request": ["moody_blue", "dark_blue", "violet", "light_red", "ceramic", "orange_yellow", "grey_green", "cyan", "black"],
            "dataset": query_id,
            "dataset_type": "query"
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
        console.log('Global CCS Ready to launch visualisation');
        var complete_url = "/visualiser/show_line_chart?" + url;
        viz_frame.attr('src', complete_url);
        viz_frame.on('load', function () {
            console.log('Global CCS Visualisation Completed');
            $(this).show();
            $.ajax({
                url: "/data_manager/delete_query",
                type: "POST",
                data: JSON.stringify(query_id),
                contentType: 'application/json',
                success: function (data) {
                    console.log("Global CCS Temporary Query Deleted");
                },
                error: function (data) {
                    console.log(data);
                }
            });

            $('#ccs_loading_bar').hide();

        });

    }


    function create_query(variable, scenarios, regions, models, period_start, period_end, min_max_list) {
        const input_dict = {
            'scenario__name': scenarios,
            'variable__name': variable,
            'region__name': regions,
            'model__name': models
        };
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

            and_dict.push({
                'operand_1': selected[j],
                'operand_2': temp,
                'operation': 'in'
            });
        }

        and_dict.push({
            'operand_1': 'year',
            'operand_2': period_start,
            'operation': '>='
        });
        and_dict.push({
            'operand_1': 'year',
            'operand_2': period_end,
            'operation': '<='
        });
        and_dict.push({
            'operand_1': 'value',
            'operand_2': 0,
            'operation': '>'
        });


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
                        "parameter": "model__name",
                        "ascending": true
                    },
                    {
                        "parameter": "scenario__name",
                        "ascending": true
                    },
                    {
                        "parameter": "year",
                        "ascending": true
                    }
                ]
                ,
                "grouping": {"params": [], "aggregated_params": []},
            },
            "additional_app_parameters": {}

        };
        console.log(query_data);

        return {
            "models": models,
            "regions": regions,
            "scenarios": scenarios,
            "variables": variable,
            "query_data": query_data,
            "min_max_list": min_max_list
        }

    }

    function retrieve_series_info_global_ccs_1(jq_obj) {
        const units_info = {
            "model_name": jq_obj["models"],
            "variable_name": jq_obj["variables"],
            "scenario_name": jq_obj["scenarios"],
            "region_name": jq_obj["regions"],
            "dataset": 'i2amparis_main_resultscomp'
        };
        var instances = [];
        var final_val_list = [];
        var final_title_list = [];
        var final_unit_list = [];
        $.ajax({
            url: "/data_manager/retrieve_series_model_scenario",
            type: "POST",
            data: JSON.stringify(units_info),
            contentType: 'application/json',
            success: function (data) {
                console.log('Global CCS 1 Unit Info Retrieved');
                instances = data["instances"];
                for (var i = 0; i < instances.length; i++) {
                    final_val_list.push(instances[i]['series']);
                    final_title_list.push(instances[i]['title']);
                    final_unit_list.push(instances[i]['unit']);
                }
                var json_object = {
                    "data": jq_obj['query_data'],
                    "val_list": final_val_list,
                    "title_list": final_title_list,
                    "unit_list": final_unit_list
                };
                start_qc_v_global_ccs_1_process(json_object, jq_obj['variables'])

            },
            error: function (data) {
                console.log(data);
            }
        });

    }


});

