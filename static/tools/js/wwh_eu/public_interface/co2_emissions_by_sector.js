$(document).ready(function () {

    function run_energy_co2_emissions_by_sector() {
        var viz_frame = $('#energy_co2_emissions_by_sector_viz_frame_div');
        viz_frame.show();
        /* Token Retrieval*/
        const csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        });
        /* # Query creation*/
        var jq_obj = create_energy_co2_emissions_by_sector_query();
        console.log(jq_obj);
        console.log('CO2 Emissions by sector JSON Query Created');
        start_qc_v_energy_co2_emissions_by_sector_process(jq_obj);


    };

    function start_qc_v_energy_co2_emissions_by_sector_process(json_query_obj) {
        var query = {};
        query["query_name"] = "wwheu_pub_emissions_by_sector_query";
        query["parameters"] = json_query_obj['query_data'];
        $.ajax({
            url: "/data_manager/create_query",
            type: "POST",
            data: JSON.stringify(query),
            contentType: 'application/json',
            success: function (data) {
                console.log('CO2 Emissions by sector Query Saved in DB');
                var query_id = data['query_id'];
                create_visualisation_energy_co2_emissions_by_sector(query_id);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }


    function create_visualisation_energy_co2_emissions_by_sector(query_id) {
        var viz_frame = $('#energy_co2_emissions_by_sector_viz_iframe');
        viz_frame.off();
        viz_frame.hide();
        $('#energy_co2_emissions_by_sector_loading_bar').show();

        var data = {
            "y_var_names": ['ALADIN_Emissions|CO2|Energy|Supply', 'ALADIN_Emissions|CO2|Energy|Demand|Industry', 'ALADIN_Emissions|CO2|Energy|Demand|Buildings', 'ALADIN_Emissions|CO2|Energy|Demand|Transportation', 'ALADIN_Emissions|CO2|Energy|Demand|AFOFI', 'ALADIN_Emissions|CO2|Energy|Demand|Other Sector', 'E3ME_Emissions|CO2|Energy|Supply', 'E3ME_Emissions|CO2|Energy|Demand|Industry', 'E3ME_Emissions|CO2|Energy|Demand|Buildings', 'E3ME_Emissions|CO2|Energy|Demand|Transportation', 'E3ME_Emissions|CO2|Energy|Demand|AFOFI', 'E3ME_Emissions|CO2|Energy|Demand|Other Sector', 'EU-TIMES_Emissions|CO2|Energy|Supply', 'EU-TIMES_Emissions|CO2|Energy|Demand|Industry', 'EU-TIMES_Emissions|CO2|Energy|Demand|Buildings', 'EU-TIMES_Emissions|CO2|Energy|Demand|Transportation', 'EU-TIMES_Emissions|CO2|Energy|Demand|AFOFI', 'EU-TIMES_Emissions|CO2|Energy|Demand|Other Sector', 'FORECAST_Emissions|CO2|Energy|Supply', 'FORECAST_Emissions|CO2|Energy|Demand|Industry', 'FORECAST_Emissions|CO2|Energy|Demand|Buildings', 'FORECAST_Emissions|CO2|Energy|Demand|Transportation', 'FORECAST_Emissions|CO2|Energy|Demand|AFOFI', 'FORECAST_Emissions|CO2|Energy|Demand|Other Sector', '42_Emissions|CO2|Energy|Supply', '42_Emissions|CO2|Energy|Demand|Industry', '42_Emissions|CO2|Energy|Demand|Buildings', '42_Emissions|CO2|Energy|Demand|Transportation', '42_Emissions|CO2|Energy|Demand|AFOFI', '42_Emissions|CO2|Energy|Demand|Other Sector', 'GCAM_Emissions|CO2|Energy|Supply', 'GCAM_Emissions|CO2|Energy|Demand|Industry', 'GCAM_Emissions|CO2|Energy|Demand|Buildings', 'GCAM_Emissions|CO2|Energy|Demand|Transportation', 'GCAM_Emissions|CO2|Energy|Demand|AFOFI', 'GCAM_Emissions|CO2|Energy|Demand|Other Sector', 'Gemini-E3_Emissions|CO2|Energy|Supply', 'Gemini-E3_Emissions|CO2|Energy|Demand|Industry', 'Gemini-E3_Emissions|CO2|Energy|Demand|Buildings', 'Gemini-E3_Emissions|CO2|Energy|Demand|Transportation', 'Gemini-E3_Emissions|CO2|Energy|Demand|AFOFI', 'Gemini-E3_Emissions|CO2|Energy|Demand|Other Sector', 'ICES_Emissions|CO2|Energy|Supply', 'ICES_Emissions|CO2|Energy|Demand|Industry', 'ICES_Emissions|CO2|Energy|Demand|Buildings', 'ICES_Emissions|CO2|Energy|Demand|Transportation', 'ICES_Emissions|CO2|Energy|Demand|AFOFI', 'ICES_Emissions|CO2|Energy|Demand|Other Sector', 'MUSE_Emissions|CO2|Energy|Supply', 'MUSE_Emissions|CO2|Energy|Demand|Industry', 'MUSE_Emissions|CO2|Energy|Demand|Buildings', 'MUSE_Emissions|CO2|Energy|Demand|Transportation', 'MUSE_Emissions|CO2|Energy|Demand|AFOFI', 'MUSE_Emissions|CO2|Energy|Demand|Other Sector', 'NEMESIS_Emissions|CO2|Energy|Supply', 'NEMESIS_Emissions|CO2|Energy|Demand|Industry', 'NEMESIS_Emissions|CO2|Energy|Demand|Buildings', 'NEMESIS_Emissions|CO2|Energy|Demand|Transportation', 'NEMESIS_Emissions|CO2|Energy|Demand|AFOFI', 'NEMESIS_Emissions|CO2|Energy|Demand|Other Sector', 'TIAM_Emissions|CO2|Energy|Supply', 'TIAM_Emissions|CO2|Energy|Demand|Industry', 'TIAM_Emissions|CO2|Energy|Demand|Buildings', 'TIAM_Emissions|CO2|Energy|Demand|Transportation', 'TIAM_Emissions|CO2|Energy|Demand|AFOFI', 'TIAM_Emissions|CO2|Energy|Demand|Other Sector'],
            "y_var_titles": ['Emissions|CO2|Energy|Supply', 'Emissions|CO2|Energy|Demand|Industry', 'Emissions|CO2|Energy|Demand|Buildings', 'Emissions|CO2|Energy|Demand|Transportation', 'Emissions|CO2|Energy|Demand|AFOFI', 'Emissions|CO2|Energy|Demand|Other Sector', 'Emissions|CO2|Energy|Supply', 'Emissions|CO2|Energy|Demand|Industry', 'Emissions|CO2|Energy|Demand|Buildings', 'Emissions|CO2|Energy|Demand|Transportation', 'Emissions|CO2|Energy|Demand|AFOFI', 'Emissions|CO2|Energy|Demand|Other Sector', 'Emissions|CO2|Energy|Supply', 'Emissions|CO2|Energy|Demand|Industry', 'Emissions|CO2|Energy|Demand|Buildings', 'Emissions|CO2|Energy|Demand|Transportation', 'Emissions|CO2|Energy|Demand|AFOFI', 'Emissions|CO2|Energy|Demand|Other Sector', 'Emissions|CO2|Energy|Supply', 'Emissions|CO2|Energy|Demand|Industry', 'Emissions|CO2|Energy|Demand|Buildings', 'Emissions|CO2|Energy|Demand|Transportation', 'Emissions|CO2|Energy|Demand|AFOFI', 'Emissions|CO2|Energy|Demand|Other Sector', 'Emissions|CO2|Energy|Supply', 'Emissions|CO2|Energy|Demand|Industry', 'Emissions|CO2|Energy|Demand|Buildings', 'Emissions|CO2|Energy|Demand|Transportation', 'Emissions|CO2|Energy|Demand|AFOFI', 'Emissions|CO2|Energy|Demand|Other Sector', 'Emissions|CO2|Energy|Supply', 'Emissions|CO2|Energy|Demand|Industry', 'Emissions|CO2|Energy|Demand|Buildings', 'Emissions|CO2|Energy|Demand|Transportation', 'Emissions|CO2|Energy|Demand|AFOFI', 'Emissions|CO2|Energy|Demand|Other Sector', 'Emissions|CO2|Energy|Supply', 'Emissions|CO2|Energy|Demand|Industry', 'Emissions|CO2|Energy|Demand|Buildings', 'Emissions|CO2|Energy|Demand|Transportation', 'Emissions|CO2|Energy|Demand|AFOFI', 'Emissions|CO2|Energy|Demand|Other Sector', 'Emissions|CO2|Energy|Supply', 'Emissions|CO2|Energy|Demand|Industry', 'Emissions|CO2|Energy|Demand|Buildings', 'Emissions|CO2|Energy|Demand|Transportation', 'Emissions|CO2|Energy|Demand|AFOFI', 'Emissions|CO2|Energy|Demand|Other Sector', 'Emissions|CO2|Energy|Supply', 'Emissions|CO2|Energy|Demand|Industry', 'Emissions|CO2|Energy|Demand|Buildings', 'Emissions|CO2|Energy|Demand|Transportation', 'Emissions|CO2|Energy|Demand|AFOFI', 'Emissions|CO2|Energy|Demand|Other Sector', 'Emissions|CO2|Energy|Supply', 'Emissions|CO2|Energy|Demand|Industry', 'Emissions|CO2|Energy|Demand|Buildings', 'Emissions|CO2|Energy|Demand|Transportation', 'Emissions|CO2|Energy|Demand|AFOFI', 'Emissions|CO2|Energy|Demand|Other Sector', 'Emissions|CO2|Energy|Supply', 'Emissions|CO2|Energy|Demand|Industry', 'Emissions|CO2|Energy|Demand|Buildings', 'Emissions|CO2|Energy|Demand|Transportation', 'Emissions|CO2|Energy|Demand|AFOFI', 'Emissions|CO2|Energy|Demand|Other Sector'],
            "y_var_units": ['MtCO2/y'],
            "y_axis_title": 'CO2 Emissions',
            "x_axis_name": "year",
            "x_axis_title": "Year",
            "x_axis_unit": "-",
            "x_axis_type": "text",
            "cat_axis_names": ['aladin', 'e3me', 'eu_times', 'forecast', '42', 'gcam', 'gemini_e3', 'ices', 'muse', 'nemesis', 'tiam'],
            "cat_axis_titles": ['ALADIN', 'E3ME', 'EU-TIMES', 'FORECAST', '42', 'GCAM', 'Gemini-E3', 'ICES', 'MUSE', 'NEMESIS', 'TIAM'],
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
        console.log('Global Primary Energy Ready to launch visualisation');
        var complete_url = "/visualiser/show_stacked_clustered_column_chart?" + url;
        viz_frame.attr('src', complete_url);
        viz_frame.on('load', function () {
            console.log('CO2 Emissions by sector Visualisation Completed');
            $(this).show();
            $.ajax({
                url: "/data_manager/delete_query",
                type: "POST",
                data: JSON.stringify(query_id),
                contentType: 'application/json',
                success: function (data) {
                    console.log("CO2 Emissions by sector Temporary Query Deleted");
                },
                error: function (data) {
                    console.log(data);
                }
            });

            $('#energy_co2_emissions_by_sector_loading_bar').hide();

        });

    }

    function create_energy_co2_emissions_by_sector_query() {
        var regions = ['EU'];
        var models = ['aladin', 'e3me', 'eu_times', 'forecast', '42', 'gcam', 'gemini_e3', 'ices', 'muse', 'nemesis', 'tiam'];
        var variables = ['Emissions|CO2|Energy|Supply', 'Emissions|CO2|Energy|Demand|Industry', 'Emissions|CO2|Energy|Demand|Buildings', 'Emissions|CO2|Energy|Demand|Transportation', 'Emissions|CO2|Energy|Demand|AFOFI', 'Emissions|CO2|Energy|Demand|Other Sector'];
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

    run_energy_co2_emissions_by_sector();




});

