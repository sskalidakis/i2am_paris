$(document).ready(function () {

    $("#ccs2-clear-button").click(function () {
        $('#ccs2 select.sum-boot-select').multipleSelect('setSelects', []);
        $('#ccs2_viz_frame_div').hide();
    });

    $("#ccs2-run-button").click(function () {
        var viz_id = 'ccs2';
        var viz_type = 'show_line_chart';
        var intrfc = 'eu_wwh_scientific';
        var dataset = 'i2amparis_main_wwheuresultscomp';
        var viz_frame = $('#' + viz_id + '_viz_frame_div');
        var model_sel = $('#ccs2_model_name');
        var model_full = (model_sel.multipleSelect('getSelects').length === 0);
        if (model_full) {
            alert('Please, select at least one value from each field to update the visualisation.')
        } else {
            viz_frame.show();
            token_retrieval();

            /* # Query creation*/
            var jq_obj = create_ccs2_query(dataset);
            console.log(viz_id + ' - JSON Query Created');
            var y_var_names = model_sel.multipleSelect('getSelects');
            var y_var_titles = model_sel.multipleSelect('getSelects','text');
            var viz_payload = {
                "y_var_names": y_var_names,
                "y_var_titles": y_var_titles,
                "y_var_units": ['MtCO2/y'],
                "y_axis_title": 'CO2 Captured',
                "x_axis_name": "Extra_CO2_reduction_ratio",
                "x_axis_title": "CO2 emissions reduction",
                "x_axis_unit": "percentage %",
                "x_axis_type": "value",
                "use_default_colors": false,
                "color_list_request": ["moody_blue", "dark_blue", "violet", "light_red", "ceramic", "orange_yellow", "grey_green", "cyan", "black"],
                "dataset_type": "query",
            };
            start_sci_query_creation_viz_execution(jq_obj, viz_id, viz_payload, viz_type, intrfc)
        }
    });


    function create_ccs2_query(dataset) {
        var sel_model = $('#ccs2_model_name');
        var variable = ['Extra_CO2_Captured_with_CCS', 'Extra_CO2_reduction_ratio'];
        const models = sel_model.multipleSelect('getSelects');
        const scenarios = ['EUWWH'];
        const regions = ['EU']

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


    $("#ccs2-run-button").trigger('click');
});

