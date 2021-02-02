$(document).ready(function () {

    $("#global_primary_energy-clear-button").click(function () {
        $('#global_primary_energy select.sum-boot-select').multipleSelect('setSelects', []);
        $('#global_primary_energy_viz_frame_div').hide();
    });

    $("#global_primary_energy-run-button").click(function () {
        var viz_frame = $('#global_primary_energy_viz_frame_div');
        var model_sel = $('#global_primary_energy_model_name');
        var scenario_sel = $('#global_primary_energy_scenario_name');
        var variable_sel = $('#global_primary_energy_variable_name');
        var model_full = (model_sel.multipleSelect('getSelects').length === 0);
        var scenario_full = (scenario_sel.multipleSelect('getSelects').length === 0);
        var variable_full = (variable_sel.multipleSelect('getSelects').length === 0);
        if (model_full || scenario_full || variable_full) {
            alert('Please, select at least one value from each field to update the visualisation.')
        } else {
            viz_frame.show();
            /* Token Retrieval*/
            const csrftoken = getCookie('csrftoken');
            $.ajaxSetup({
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            });

            /* # Query creation*/
            var jq_obj = create_global_primary_energy_query();
            console.log('Global Primary Energy JSON Query Created');
            retrieve_series_info_global_primary_energy(jq_obj);

        }
    });

    function start_qc_v_global_primary_energy_process(json_query_obj, variable){
        var query = {};
        query["query_name"] = "global_primary_energy_query";
        query["parameters"] = json_query_obj['data'];
        // var variable_selection = (variable_sel.multipleSelect('getSelects', 'text'));
        $.ajax({
            url: "/data_manager/create_query",
            type: "POST",
            data: JSON.stringify(query),
            contentType: 'application/json',
            success: function (data) {
                console.log('Global Primary Energy Query Saved in DB');
                var query_id = data['query_id'];
                create_visualisation_global_primary_energy(query_id, json_query_obj['val_list'], json_query_obj['title_list'], json_query_obj['unit_list'], variable);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }


    function create_visualisation_global_primary_energy(query_id, val_list, title_list, unit_list, variable) {
        var viz_frame = $('#global_primary_energy_viz_iframe');
        viz_frame.off();
        viz_frame.hide();
        $('#global_primary_energy_loading_bar').show();

        var data = {
            "y_var_names": val_list,
            "y_var_titles": title_list,
            "y_var_units": unit_list,
            "y_axis_title": 'Global '+String(variable[0]),
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
        console.log('Global Primary Energy Ready to launch visualisation');
        var complete_url = "/visualiser/show_line_chart?" + url;
        viz_frame.attr('src', complete_url);
        viz_frame.on('load', function () {
            console.log('Global Primary Energy Visualisation Completed');
            $(this).show();
            $.ajax({
                url: "/data_manager/delete_query",
                type: "POST",
                data: JSON.stringify(query_id),
                contentType: 'application/json',
                success: function (data) {
                    console.log("Global Primary Energy Temporary Query Deleted");
                },
                error: function (data) {
                    console.log(data);
                }
            });

            $('#global_primary_energy_loading_bar').hide();

        });

    }

    function create_global_primary_energy_query() {
        var sel_model = $('#global_primary_energy_model_name');
        var sel_scenario = $('#global_primary_energy_scenario_name');
        var sel_variable = $('#global_primary_energy_variable_name');
        var regions = ['World'];

        const models = sel_model.multipleSelect('getSelects');
        const scenarios = sel_scenario.multipleSelect('getSelects');
        const variables = sel_variable.multipleSelect('getSelects');

        const input_dict = {
            'model__name': models,
            'scenario__name': scenarios,
            'region__name': regions,
            'variable__name': variables
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

        return {
            "models": models,
            "variables": variables,
            "scenarios": scenarios,
            "regions": regions,
            "query_data": query_data
        }

    }

    function retrieve_series_info_global_primary_energy(jq_obj) {
        const units_info = {
            "model_name": jq_obj["models"],
            "variable_name": jq_obj["variables"],
            "scenario_name": jq_obj["scenarios"],
            "region_name": jq_obj["regions"],
        };
        var instances = [];
        var final_val_list = [];
        var final_title_list = [];
        var final_unit_list = [];
        $.ajax({
            url: "/data_manager/retrieve_series_info_fossil_energy_co2",
            type: "POST",
            data: JSON.stringify(units_info),
            contentType: 'application/json',
            success: function (data) {
                console.log('Global Primary Energy Unit Info Retrieved');
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
                start_qc_v_global_primary_energy_process(json_object, jq_obj['variables'])

            },
            error: function (data) {
                console.log(data);
            }
        });

    }

    $("#global_primary_energy-run-button").trigger('click');
});

