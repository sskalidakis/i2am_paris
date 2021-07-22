$(document).ready(function () {


    var viz_frame = $('#imported_fuels_viz_frame_div');

    viz_frame.show();
    /* Token Retrieval*/
    const csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    });

    /* # Query creation*/
    var jq_obj = create_imported_fuels_query();
    console.log('Imported Fuels JSON Query Created');
    start_qc_v_imported_fuels_process(jq_obj)


    function start_qc_v_imported_fuels_process(json_query_obj) {
        var query = {};
        query["query_name"] = "wwheu_pub_imported_fuels_query";
        query["parameters"] = json_query_obj['query_data'];
        $.ajax({
            url: "/data_manager/create_query",
            type: "POST",
            data: JSON.stringify(query),
            contentType: 'application/json',
            success: function (data) {
                console.log('Imported Fuels Query Saved in DB');
                var query_id = data['query_id'];
                create_visualisation_imported_fuels(query_id);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }


    function create_visualisation_imported_fuels(query_id) {
        var viz_frame = $('#imported_fuels_viz_iframe');
        viz_frame.off();
        viz_frame.hide();
        $('#imported_fuels_loading_bar').show();

        var data = {
            "y_var_names": ['eu_times_Trade|Primary Energy|Coal|Volume', 'eu_times_Trade|Primary Energy|Gas|Volume', 'eu_times_Trade|Primary Energy|Oil|Volume', 'gemini_e3_Trade|Primary Energy|Coal|Volume', 'gemini_e3_Trade|Primary Energy|Gas|Volume', 'gemini_e3_Trade|Primary Energy|Oil|Volume', 'tiam_Trade|Primary Energy|Coal|Volume', 'tiam_Trade|Primary Energy|Gas|Volume', 'tiam_Trade|Primary Energy|Oil|Volume', 'gcam_Trade|Primary Energy|Coal|Volume', 'gcam_Trade|Primary Energy|Gas|Volume', 'gcam_Trade|Primary Energy|Oil|Volume'],
            "y_var_titles": ['EU-TIMES - Trade|Primary Energy|Coal|Volume', 'EU-TIMES - Trade|Primary Energy|Gas|Volume', 'EU-TIMES - Trade|Primary Energy|Oil|Volume', 'Gemini-E3 - Trade|Primary Energy|Coal|Volume', 'Gemini-E3 - Trade|Primary Energy|Gas|Volume', 'Gemini-E3 - Trade|Primary Energy|Oil|Volume', 'TIAM - Trade|Primary Energy|Coal|Volume', 'TIAM - Trade|Primary Energy|Gas|Volume', 'TIAM - Trade|Primary Energy|Oil|Volume', 'GCAM - Trade|Primary Energy|Coal|Volume', 'GCAM - Trade|Primary Energy|Gas|Volume', 'GCAM - Trade|Primary Energy|Oil|Volume'],
            "y_var_units": ['billion US$2010/yr OR local currency', 'billion US$2010/yr OR local currency', 'billion US$2010/yr OR local currency', 'billion US$2010/yr OR local currency', 'billion US$2010/yr OR local currency', 'billion US$2010/yr OR local currency', 'billion US$2010/yr OR local currency', 'billion US$2010/yr OR local currency', 'billion US$2010/yr OR local currency'],
            "y_axis_title": 'Imported fossil fuels',
            "x_axis_name": "year",
            "x_axis_title": "Year",
            "x_axis_unit": "-",
            "x_axis_type": "text",
            "use_default_colors": false,
            "color_list_request": ["black","dark_blue", "dark_green", "dark_gray",  "blue", "green", "gray", "light_blue", "light_green", "ice_gray", "lighter_blue", "lighter_green"],
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
        console.log('Imported Fuels Ready to launch visualisation');
        var complete_url = "/visualiser/show_line_chart?" + url;
        viz_frame.attr('src', complete_url);
        viz_frame.on('load', function () {
            console.log('Imported Fuels Visualisation Completed');
            $(this).show();
            $.ajax({
                url: "/data_manager/delete_query",
                type: "POST",
                data: JSON.stringify(query_id),
                contentType: 'application/json',
                success: function (data) {
                    console.log("Imported Fuels Query Deleted");
                },
                error: function (data) {
                    console.log(data);
                }
            });

            $('#imported_fuels_loading_bar').hide();

        });

    }

    function create_imported_fuels_query() {
        var models = ['eu_times', 'gemini_e3', 'tiam', 'gcam'];
        var scenarios = ['PR_CurPol_CP', 'PR_WWH_CP'];
        var regions = ['EU'];
        var variable = ['Trade|Primary Energy|Coal|Volume', 'Trade|Primary Energy|Gas|Volume','Trade|Primary Energy|Oil|Volume'];


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

