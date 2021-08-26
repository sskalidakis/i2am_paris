$(document).ready(function () {
    var viz_id = 'hydrogen_electricity_comp_trans';
    var viz_type = 'show_stacked_clustered_column_chart';
    var intrfc = 'wwheu_pub';
    var viz_frame = $('#' + viz_id + '_viz_frame_div');
    viz_frame.show();
    token_retrieval();

    /* # Query creation*/
    var jq_obj = create_hydrogen_electricity_comp_trans_query();
    console.log(viz_id + '- JSON Query Created');
    var viz_payload = {
            "y_var_names": ['EU-TIMES_Final Energy|Transportation|Electricity', 'EU-TIMES_Final Energy|Transportation|Gases', 'EU-TIMES_Final Energy|Transportation|Hydrogen', 'EU-TIMES_Final Energy|Transportation|Liquids', 'EU-TIMES_Final Energy|Transportation|Liquids|Bioenergy', 'EU-TIMES_Final Energy|Transportation|Liquids|Biomass', 'EU-TIMES_Final Energy|Transportation|Liquids|Fossil synfuel', 'EU-TIMES_Final Energy|Transportation|Liquids|Oil', 'FORECAST_Final Energy|Transportation|Electricity', 'FORECAST_Final Energy|Transportation|Gases', 'FORECAST_Final Energy|Transportation|Hydrogen', 'FORECAST_Final Energy|Transportation|Liquids', 'FORECAST_Final Energy|Transportation|Liquids|Bioenergy', 'FORECAST_Final Energy|Transportation|Liquids|Biomass', 'FORECAST_Final Energy|Transportation|Liquids|Fossil synfuel', 'FORECAST_Final Energy|Transportation|Liquids|Oil', 'GCAM_Final Energy|Transportation|Electricity', 'GCAM_Final Energy|Transportation|Gases', 'GCAM_Final Energy|Transportation|Hydrogen', 'GCAM_Final Energy|Transportation|Liquids', 'GCAM_Final Energy|Transportation|Liquids|Bioenergy', 'GCAM_Final Energy|Transportation|Liquids|Biomass', 'GCAM_Final Energy|Transportation|Liquids|Fossil synfuel', 'GCAM_Final Energy|Transportation|Liquids|Oil', 'TIAM_Final Energy|Transportation|Electricity', 'TIAM_Final Energy|Transportation|Gases', 'TIAM_Final Energy|Transportation|Hydrogen', 'TIAM_Final Energy|Transportation|Liquids', 'TIAM_Final Energy|Transportation|Liquids|Bioenergy', 'TIAM_Final Energy|Transportation|Liquids|Biomass', 'TIAM_Final Energy|Transportation|Liquids|Fossil synfuel', 'TIAM_Final Energy|Transportation|Liquids|Oil'],
            "y_var_titles": ['Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Hydrogen', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Liquids|Bioenergy', 'Final Energy|Transportation|Liquids|Biomass', 'Final Energy|Transportation|Liquids|Fossil synfuel', 'Final Energy|Transportation|Liquids|Oil', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Hydrogen', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Liquids|Bioenergy', 'Final Energy|Transportation|Liquids|Biomass', 'Final Energy|Transportation|Liquids|Fossil synfuel', 'Final Energy|Transportation|Liquids|Oil', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Hydrogen', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Liquids|Bioenergy', 'Final Energy|Transportation|Liquids|Biomass', 'Final Energy|Transportation|Liquids|Fossil synfuel', 'Final Energy|Transportation|Liquids|Oil', 'Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Hydrogen', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Liquids|Bioenergy', 'Final Energy|Transportation|Liquids|Biomass', 'Final Energy|Transportation|Liquids|Fossil synfuel', 'Final Energy|Transportation|Liquids|Oil'],
            "y_var_units": ['EJ/yr'],
            "y_axis_title": "Final Energy in Transportation",
            "x_axis_name": "year",
            "x_axis_title": "Year",
            "x_axis_unit": "-",
            "x_axis_type": "text",
            "cat_axis_names": ['eu_times', 'forecast', 'gcam', 'tiam'],
            "cat_axis_titles": ['EU-TIMES', 'FORECAST', 'GCAM', 'TIAM'],
            "use_default_colors": false,
            "color_list_request": ["light_blue", "gray", "casual_green", "lighter_blue", "light_blue", "moody_blue", "dark_blue", "dark_gray"],
            "dataset_type": "query",
            "type": "step_by_step"
        };
    start_query_creation_viz_execution(jq_obj, viz_id, viz_payload, viz_type, intrfc)


    function create_hydrogen_electricity_comp_trans_query() {
        var regions = ['EU'];
        var models = ['eu_times', 'forecast', 'gcam', 'tiam'];
        var scenarios = ['PR_CurPol_CP', 'PR_WWH_CP'];
        var variables = ['Final Energy|Transportation|Electricity', 'Final Energy|Transportation|Gases', 'Final Energy|Transportation|Hydrogen', 'Final Energy|Transportation|Liquids', 'Final Energy|Transportation|Liquids|Bioenergy', 'Final Energy|Transportation|Liquids|Biomass', 'Final Energy|Transportation|Liquids|Fossil synfuel', 'Final Energy|Transportation|Liquids|Oil'];
        var agg_var = 'model_id';
        var agg_func = 'Avg';

        const input_dict = {
            'model__name': models,
            'region__name': regions,
            'variable__name': variables,
            'scenario__name': scenarios
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
                    "params": [agg_var, "variable__name", "year", "region__name", "scenario__name"],
                    "aggregated_params": [{"name": "value", "agg_func": agg_func}]
                },

            },
            "additional_app_parameters": {}

        };

        return {
            "models": models,
            "variables": variables,
            "regions": regions,
            "scenarios": scenarios,
            "query_data": query_data
        }

    }




});

