$(document).ready(function () {


    var viz_frame = $('#electrification_ir_co2_reduction_viz_frame_div');

    viz_frame.show();
    /* Token Retrieval*/
    const csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    });

    /* # Query creation*/
    var jq_obj = create_electrification_ir_co2_reduction_query();
    console.log('electrification_ir_co2_reduction JSON Query Created');
    start_qc_v_electrification_ir_co2_reduction_process(jq_obj)

    // retrieve_series_info_total_co2_emissions(jq_obj);


    function start_qc_v_electrification_ir_co2_reduction_process(json_query_obj) {
        var query = {};
        query["query_name"] = "wwheu_pub_electrification_ir_co2_reduction";
        query["parameters"] = json_query_obj['query_data'];
        $.ajax({
            url: "/data_manager/create_query",
            type: "POST",
            data: JSON.stringify(query),
            contentType: 'application/json',
            success: function (data) {
                console.log('electrification_ir_co2_reduction Query Saved in DB');
                var query_id = data['query_id'];
                create_visualisation_electrification_ir_co2_reduction(query_id);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }


    function create_visualisation_electrification_ir_co2_reduction(query_id) {
        var viz_frame = $('#electrification_ir_co2_reduction_viz_iframe');
        viz_frame.off();
        viz_frame.hide();
        $('#electrification_ir_co2_reduction_loading_bar').show();

        var data = {
            "y_var_names": ['tiam', 'eu_times', 'e3me', 'gcam', 'gemini_e3', 'muse', 'nemesis', '42', 'ices'],
            "y_var_titles": ['TIAM', 'EU-TIMES', 'E3ME', 'GCAM', 'Gemini-E3', 'MUSE', 'NEMESIS', '42', 'ICES'],
            "y_var_units": ['Percentage %'],
            "y_axis_title": 'Electricity in Transport',
            "x_axis_name": "Extra_CO2_reduction_ratio",
            "x_axis_title": "CO2 emissions reduction",
            "x_axis_unit": "percentage %",
            "x_axis_type": "value",
            "color_list_request": ["moody_blue", "dark_blue", "violet", "light_red", "ceramic", "orange_yellow", "grey_green", "cyan", "black"],
            "dataset": query_id,
            "dataset_type": "query",
            "type": "step_by_step"
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
        console.log('electrification_ir_co2_reduction Ready to launch visualisation');
        var complete_url = "/visualiser/show_line_chart?" + url;
        viz_frame.attr('src', complete_url);
        viz_frame.on('load', function () {
            console.log('electrification_ir_co2_reduction Visualisation Completed');
            $(this).show();
            $.ajax({
                url: "/data_manager/delete_query",
                type: "POST",
                data: JSON.stringify(query_id),
                contentType: 'application/json',
                success: function (data) {
                    console.log("electrification_ir_co2_reduction Query Deleted");
                },
                error: function (data) {
                    console.log(data);
                }
            });

            $('#electrification_ir_co2_reduction_loading_bar').hide();

        });

    }

    function create_electrification_ir_co2_reduction_query() {
        var models = ['tiam', 'eu_times', 'e3me', 'gcam', 'gemini_e3', 'muse', 'nemesis', '42', 'ices'];
        var scenarios = ['PR_CurPol_CP', 'PR_WWH_CP', 'PR_CurPol_EI'];
        var regions = ['EU'];
        var variable = ['Extra_Electricity_Share', 'Extra_CO2_reduction_ratio'];


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
                "ordering": []
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

