$(document).ready(function () {

    $("#primary_by_fuel-clear-button").click(function () {
        $('#primary_by_fuel select.sum-boot-select').multipleSelect('setSelects', []);
        $('#primary_by_fuel_viz_frame_div').hide();
    });

    $("#primary_by_fuel-run-button").click(function () {
        var viz_id = 'primary_by_fuel';
        var viz_type = 'show_stacked_clustered_column_chart';
        var intrfc = 'eu_wwh_scientific';
        var dataset = 'i2amparis_main_wwheuresultscomp';
        var viz_frame = $('#' + viz_id + '_viz_frame_div');
        var model_sel = $('#primary_by_fuel_model_name');
        var model_full = (model_sel.multipleSelect('getSelects').length === 0);
        if (model_full) {
            alert('Please, select at least one value from each field to update the visualisation.')
        } else {
            viz_frame.show();
            token_retrieval();

            /* # Query creation*/
            var jq_obj = create_primary_by_fuel_query(dataset);
            console.log(viz_id + ' - JSON Query Created');
            var y_var_models = model_sel.multipleSelect('getSelects');
            var y_var_mod_titles = model_sel.multipleSelect('getSelects', 'text');
            var variables = ['Primary Energy|Oil',
                'Primary Energy|Coal',
                'Primary Energy|Gas',
                'Primary Energy|Hydro',
                'Primary Energy|Nuclear',
                'Primary Energy|Biomass',
                'Primary Energy|Solar',
                'Primary Energy|Wind',
                'Primary Energy|Other']
            var y_var_names = []
            var y_var_titles = []
            for (var i = 0; i < y_var_models.length; i++) {
                for (var j = 0; j < variables.length; j++) {
                    y_var_names.push(String(y_var_mod_titles[i]) + '_' + variables[j]);
                    y_var_titles.push(variables[j]);
                }
            }

            var viz_payload = {
                "y_var_names": y_var_names,
                "y_var_titles": y_var_titles,
                "y_var_units": ['EJ/y'],
                "y_axis_title": 'Primary Energy',
                "x_axis_name": "year",
                "x_axis_title": "Year",
                "x_axis_unit": "-",
                "x_axis_type": "text",
                "cat_axis_names": y_var_models,
                "cat_axis_titles": y_var_mod_titles,
                "use_default_colors": false,
                "color_list_request": ["dark_gray", "gray", "grey_green", "light_blue", "purple_new", "light_brown","gold", "cyan", "ceramic"],
                "dataset_type": "query",
                "type": "normal"
            };

            start_sci_query_creation_viz_execution(jq_obj, viz_id, viz_payload, viz_type, intrfc)
        }
    });


    function create_primary_by_fuel_query(dataset) {
        var sel_model = $('#primary_by_fuel_model_name');
        var variables = ['Primary Energy|Oil',
            'Primary Energy|Coal',
            'Primary Energy|Gas',
            'Primary Energy|Hydro',
            'Primary Energy|Nuclear',
            'Primary Energy|Biomass',
            'Primary Energy|Solar',
            'Primary Energy|Wind',
            'Primary Energy|Other'];
        const models = sel_model.multipleSelect('getSelects');
        const regions = ['EU']
        var agg_var = 'model_id';
        var agg_func = 'Avg';

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
            "dataset": dataset,
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
            "regions": regions,
            "variables": variables,
            "query_data": query_data
        }

    }


    $("#primary_by_fuel-run-button").trigger('click');
});

