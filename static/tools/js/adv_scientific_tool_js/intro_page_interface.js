$(document).ready(function () {
    $('select.sum-boot-select').each(function () {
        var select = $(this);
        select.multipleSelect(
            {
                filter: true,
                showClear: true,
                animate: 'fade',
                maxHeightUnit: 'row',
                maxHeight: 8,
                dropWidth: 250,
            });
    });

    $("#fossil_energy_co2-clear-button").click(function () {
        $('#fossil_energy_co2 select.sum-boot-select').multipleSelect('setSelects', []);
        $('#viz_frame_div').hide();
        $('#chart_info').show();
    });

    $("#fossil_energy_co2-run-button").click(function () {
        var viz_frame = $('#fossil_energy_co2_viz_frame_div');
        var model_sel = $('#fossil_energy_co2_model_name');
        var scenario_sel = $('#fossil_energy_co2_scenario_name');
        var region_sel = $('#fossil_energy_co2_region_name');
        var variable = 'Emissions|CO2|Energy';
        console.log(model_sel.multipleSelect('getSelects'));
        console.log(scenario_sel.multipleSelect('getSelects'));
        console.log(region_sel.multipleSelect('getSelects'));
        console.log(variable_sel.multipleSelect('getSelects'));
        var model_full = (model_sel.multipleSelect('getSelects').length === 0);
        var scenario_full = (scenario_sel.multipleSelect('getSelects').length === 0);
        var region_full = (region_sel.multipleSelect('getSelects').length === 0);
        if (model_full || scenario_full || region_full) {
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
            var query = {};
            query["query_name"] = "fossil_energy_co2_query";
            var json_query_obj = create_query(model_sel, scenario_sel, region_sel, variable);
            query["parameters"] = json_query_obj['data'];
            var variable_selection = (variable_sel.multipleSelect('getSelects', 'text'));
            $.ajax({
                url: "/data_manager/create_query",
                type: "POST",
                data: JSON.stringify(query),
                contentType: 'application/json',
                success: function (data) {
                    console.log("query created");
                    console.log(data);
                    $('.viz-container').show();
                    var query_id = data['query_id'];
                    create_visualisation(query_id, json_query_obj['val_list'], json_query_obj['title_list'], json_query_obj['unit_list'], variable_selection);
                },
                error: function (data) {
                    console.log(data);
                }
            });

        }
    });


    function create_visualisation_fossil_energy_co2(query_id, val_list, title_list, unit_list, variable) {
        var viz_frame = $('#viz_iframe');
        viz_frame.off();
        viz_frame.hide();
        $('#loading_bar').show();

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

        var complete_url = "/visualiser/show_line_chart?" + url;
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
});

function create_fossil_energy_co2_query(sel_model, sel_scenario, sel_region, variable) {

    const models = sel_model.multipleSelect('getSelects');
    const scenarios = sel_scenario.multipleSelect('getSelects');
    const regions = sel_region.multipleSelect('getSelects');

    // var multiple_field = "model";
    // var val_list = models;
    // var title_list = sel_model.multipleSelect('getSelects', 'text');
    //
    // $('select.boot-select').each(function () {
    //     if ($(this).multipleSelect('getSelects').length > 1) {
    //         multiple_field = $(this).data('dbname');
    //         val_list = $(this).multipleSelect('getSelects');
    //         title_list = $(this).multipleSelect('getSelects', 'text');
    //     }
    // });
    // if (val_list.length === 0) {
    //     val_list = []
    // }

    const input_dict = {
        'model__name': models,
        'scenario__name': scenarios,
        'region__name': regions,
        'variable__name': variable
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
                    "parameter": "year",
                    "ascending": true
                },
            ]
            ,
            "grouping": {"params": [], "aggregated_params": []},
        },
        "additional_app_parameters": {
            // "multiple_field": multiple_field,
            // "val_list": val_list,
            // "title_list": title_list
        }

    };

//Retrieve units
    return retrieve_series_info_fossil_energy_co2(models, regions, scenarios, variable,  query_data);

}

function retrieve_series_info_fossil_energy_co2(models, regions, scenarios, variable, query_data) {
    const units_info = {
        "model_name": models,
        "region_name": regions,
        "scenario_name": scenarios,
        "variable_name": variable,
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