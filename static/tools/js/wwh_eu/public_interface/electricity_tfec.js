$(document).ready(function () {
    var viz_id = 'electrification_fec';
    var viz_type = 'show_stacked_clustered_column_chart';
    var intrfc = 'wwheu_pub';
    var viz_frame = $('#' + viz_id + '_viz_frame_div');
    viz_frame.show();
    token_retrieval();

    /* # Query creation*/
    var jq_obj = create_electrification_fec_query();
    console.log(viz_id + '- JSON Query Created');
    var viz_payload = {
            "y_var_names": ['ALADIN_Final Energy|Transportation|Electricity', 'ALADIN_Final Energy|Transportation|Gases', 'ALADIN_Final Energy|Transportation|Liquids', 'ALADIN_Final Energy|Transportation|Other', 'E3ME_Final Energy|Transportation|Electricity', 'E3ME_Final Energy|Transportation|Gases', 'E3ME_Final Energy|Transportation|Liquids', 'E3ME_Final Energy|Transportation|Other', 'EU-TIMES_Final Energy|Transportation|Electricity', 'EU-TIMES_Final Energy|Transportation|Gases', 'EU-TIMES_Final Energy|Transportation|Liquids', 'EU-TIMES_Final Energy|Transportation|Other', '42_Final Energy|Transportation|Electricity', '42_Final Energy|Transportation|Gases', '42_Final Energy|Transportation|Liquids', '42_Final Energy|Transportation|Other', 'GCAM_Final Energy|Transportation|Electricity', 'GCAM_Final Energy|Transportation|Gases', 'GCAM_Final Energy|Transportation|Liquids', 'GCAM_Final Energy|Transportation|Other', 'Gemini-E3_Final Energy|Transportation|Electricity', 'Gemini-E3_Final Energy|Transportation|Gases', 'Gemini-E3_Final Energy|Transportation|Liquids', 'Gemini-E3_Final Energy|Transportation|Other', 'ICES_Final Energy|Transportation|Electricity', 'ICES_Final Energy|Transportation|Gases', 'ICES_Final Energy|Transportation|Liquids', 'ICES_Final Energy|Transportation|Other', 'MUSE_Final Energy|Transportation|Electricity', 'MUSE_Final Energy|Transportation|Gases', 'MUSE_Final Energy|Transportation|Liquids', 'MUSE_Final Energy|Transportation|Other', 'NEMESIS_Final Energy|Transportation|Electricity', 'NEMESIS_Final Energy|Transportation|Gases', 'NEMESIS_Final Energy|Transportation|Liquids', 'NEMESIS_Final Energy|Transportation|Other', 'TIAM_Final Energy|Transportation|Electricity', 'TIAM_Final Energy|Transportation|Gases', 'TIAM_Final Energy|Transportation|Liquids', 'TIAM_Final Energy|Transportation|Other'],
            "y_var_titles": ['Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Other', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Other'],
            "y_var_units": ['EJ/y'],
            "y_axis_title": 'Transport Final Energy',
            "x_axis_name": "year",
            "x_axis_title": "Year",
            "x_axis_unit": "-",
            "x_axis_type": "text",
            "cat_axis_names": ['aladin', 'e3me', 'eu_times', '42', 'gcam', 'gemini_e3', 'ices', 'muse', 'nemesis', 'tiam'],
            "cat_axis_titles": ['ALADIN', 'E3ME', 'EU-TIMES', '42', 'GCAM', 'Gemini-E3', 'ICES', 'MUSE', 'NEMESIS', 'TIAM'],
            "use_default_colors": false,
            "color_list_request": ["light_blue", "gray", "dark_gray", "grey_green"],
            "dataset_type": "query",
            "type": "step_by_step"
        };

    start_query_creation_viz_execution(jq_obj, viz_id, viz_payload, viz_type, intrfc)


    function create_electrification_fec_query() {
        var regions = ['EU'];
        var models = ['aladin', 'e3me', 'eu_times', '42', 'gcam', 'gemini_e3', 'ices', 'muse', 'nemesis', 'tiam'];
        var variables = ['Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Other'];
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


});

