$(document).ready(function () {


    var viz_frame = $('#total_co2_emissions_viz_frame_div');

    viz_frame.show();
    /* Token Retrieval*/
    const csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    });

    /* # Query creation*/
    var jq_obj = create_total_co2_emissions_query();
    console.log('Total_co2_emissions JSON Query Created');
    start_qc_v_total_co2_emissions_process(jq_obj)

    // retrieve_series_info_total_co2_emissions(jq_obj);


    function start_qc_v_total_co2_emissions_process(json_query_obj) {
        var query = {};
        query["query_name"] = "wwheu_pub_total_co2_emissions_query";
        query["parameters"] = json_query_obj['query_data'];
        // var variable_selection = (variable_sel.multipleSelect('getSelects', 'text'));
        $.ajax({
            url: "/data_manager/create_query",
            type: "POST",
            data: JSON.stringify(query),
            contentType: 'application/json',
            success: function (data) {
                console.log('Fossil Energy Query Saved in DB');
                var query_id = data['query_id'];
                create_visualisation_total_co2_emissions(query_id);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }


    function create_visualisation_total_co2_emissions(query_id) {
        var viz_frame = $('#total_co2_emissions_viz_iframe');
        viz_frame.off();
        viz_frame.hide();
        $('#total_co2_emissions_loading_bar').show();

        var data = {
            "y_var_names": ['e3me_PR_CurPol_CP', 'gcam_PR_CurPol_CP', 'gemini_e3_PR_CurPol_CP','ices_PR_CurPol_CP', 'muse_PR_CurPol_CP','tiam_PR_CurPol_CP'],
            "y_var_titles": ['E3ME- PR_CurPol_CP', 'GCAM- PR_CurPol_CP', 'Gemini-E3- PR_CurPol_CP','ICES- PR_CurPol_CP', 'MUSE- PR_CurPol_CP','TIAM- PR_CurPol_CP'],
            "y_var_units": ['MtCO2/y', 'MtCO2/y','MtCO2/y','MtCO2/y','MtCO2/y','MtCO2/y','MtCO2/y','MtCO2/y','MtCO2/y'],
            "y_axis_title": 'Emissions|CO2|Energy',
            "x_axis_name": "year",
            "x_axis_title": "Year",
            "x_axis_unit": "-",
            "x_axis_type": "text",
            "color_list_request": ["moody_blue", "violet", "light_red", "orange_yellow", "grey_green", "cyan", "black"],
            "dataset": query_id,
            "dataset_type": "query",
            "use_default_colors": false,
            // "type": "step_by_step"
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
        console.log('Total_co2_emissions Ready to launch visualisation');
        var complete_url = "/visualiser/show_line_chart?" + url;
        viz_frame.attr('src', complete_url);
        viz_frame.on('load', function () {
            console.log('Total_co2_emissions Visualisation Completed');
            $(this).show();
            $.ajax({
                url: "/data_manager/delete_query",
                type: "POST",
                data: JSON.stringify(query_id),
                contentType: 'application/json',
                success: function (data) {
                    console.log("Total_co2_emissions Query Deleted");
                },
                error: function (data) {
                    console.log(data);
                }
            });

            $('#total_co2_emissions_loading_bar').hide();

        });

    }

    function create_total_co2_emissions_query() {
        var models = ['42', 'e3me', 'eu_times', 'gcam', 'gemini_e3', 'ices', 'muse', 'nemesis', 'tiam'];
        var scenarios = ['PR_CurPol_CP', 'PR_WWH_CP', 'PR_CurPol_EI'];
        var regions = ['EU'];
        var variable = ['Emissions|CO2|Energy'];


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
            "dataset": "i2amparis_main_wwheuresultscomp",
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
            "regions": regions,
            "scenarios": scenarios,
            "variables": variable,
            "query_data": query_data
        }

    }


});

