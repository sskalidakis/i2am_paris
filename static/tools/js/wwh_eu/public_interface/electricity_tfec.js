$(document).ready(function () {

    function run_electrification_fec() {
        var viz_frame = $('#electrification_fec_viz_frame_div');
        viz_frame.show();
        /* Token Retrieval*/
        const csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        });
        /* # Query creation*/
        var jq_obj = create_electrification_fec_query();
        console.log(jq_obj);
        console.log('electrification_fec JSON Query Created');
        start_qc_v_electrification_fec_process(jq_obj);


    }

    function start_qc_v_electrification_fec_process(json_query_obj) {
        var query = {};
        query["query_name"] = "wwheu_pub_electrification_fec_query";
        query["parameters"] = json_query_obj['query_data'];
        $.ajax({
            url: "/data_manager/create_query",
            type: "POST",
            data: JSON.stringify(query),
            contentType: 'application/json',
            success: function (data) {
                console.log('CO2 Emissions by sector Query Saved in DB');
                var query_id = data['query_id'];
                create_visualisation_electrification_fec(query_id);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }


    function create_visualisation_electrification_fec(query_id) {
        var viz_frame = $('#electrification_fec_viz_iframe');
        viz_frame.off();
        viz_frame.hide();
        $('#electrification_fec_loading_bar').show();

        var data = {
            "y_var_names": ['ALADIN_Final Energy|Transportation|Electricity', 'ALADIN_Final Energy|Transportation|Other', 'E3ME_Final Energy|Transportation|Electricity', 'E3ME_Final Energy|Transportation|Other', 'EU-TIMES_Final Energy|Transportation|Electricity', 'EU-TIMES_Final Energy|Transportation|Other', '42_Final Energy|Transportation|Electricity', '42_Final Energy|Transportation|Other', 'GCAM_Final Energy|Transportation|Electricity', 'GCAM_Final Energy|Transportation|Other', 'Gemini-E3_Final Energy|Transportation|Electricity', 'Gemini-E3_Final Energy|Transportation|Other', 'ICES_Final Energy|Transportation|Electricity', 'ICES_Final Energy|Transportation|Other', 'MUSE_Final Energy|Transportation|Electricity', 'MUSE_Final Energy|Transportation|Other', 'NEMESIS_Final Energy|Transportation|Electricity', 'NEMESIS_Final Energy|Transportation|Other', 'TIAM_Final Energy|Transportation|Electricity', 'TIAM_Final Energy|Transportation|Other'],
            "y_var_titles": ['Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Other'],
            "y_var_units": ['EJ/y'],
            "y_axis_title": 'Transport Final Energy',
            "x_axis_name": "year",
            "x_axis_title": "Year",
            "x_axis_unit": "-",
            "x_axis_type": "text",
            "cat_axis_names": ['aladin', 'e3me', 'eu_times', '42', 'gcam', 'gemini_e3', 'ices', 'muse', 'nemesis', 'tiam'],
            "cat_axis_titles": ['ALADIN', 'E3ME', 'EU-TIMES', '42', 'GCAM', 'Gemini-E3', 'ICES', 'MUSE', 'NEMESIS', 'TIAM'],
            "use_default_colors": false,
            "color_list_request": ["light_blue", "gold", "blue", "casual_green", "ceramic", "petrol_blue", "red", "dark_gray", "orange_fire", "cyan", "purple_new", "ocean_dark_blue"],
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
        console.log('electrification_fec Ready to launch visualisation');
        var complete_url = "/visualiser/show_stacked_clustered_column_chart?" + url;
        viz_frame.attr('src', complete_url);
        viz_frame.on('load', function () {
            console.log('electrification_fec Visualisation Completed');
            $(this).show();
            $.ajax({
                url: "/data_manager/delete_query",
                type: "POST",
                data: JSON.stringify(query_id),
                contentType: 'application/json',
                success: function (data) {
                    console.log("electrification_fec Temporary Query Deleted");
                },
                error: function (data) {
                    console.log(data);
                }
            });

            $('#electrification_fec_loading_bar').hide();

        });

    }

    function create_electrification_fec_query() {
        var regions = ['EU'];
        var models = ['aladin', 'e3me', 'eu_times', '42', 'gcam', 'gemini_e3', 'ices', 'muse', 'nemesis', 'tiam'];
        var variables = ['Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Other'];
        var agg_func = 'Avg';
        var agg_var = 'model_id';

        const input_dict = {
            'model__name': models,
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
                        "parameter": "year",
                        "ascending": true
                    }
                ]
                ,
                "grouping": {
                    "params": [agg_var, "variable__name", "year", "region__name"],
                    "aggregated_params": [{"name": "value", "agg_func": agg_func}]
                },

            },
            "additional_app_parameters": {}

        };

        return {
            "models": models,
            "variables": variables,
            "regions": regions,
            "query_data": query_data
        }

    }

    run_electrification_fec();




});

