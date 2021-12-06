$(document).ready(function () {

    $("#co2_emissions-clear-button").click(function () {
        $('#co2_emissions select.sum-boot-select').multipleSelect('setSelects', []);
        $('#co2_emissions_viz_frame_div').hide();
    });

    $("#co2_emissions-run-button").click(function () {
        var viz_id = 'co2_emissions';
        var viz_type = 'show_line_chart';
        var intrfc = 'eu_wwh_scientific';
        var dataset = 'i2amparis_main_wwheuresultscomp';
        var viz_frame = $('#' + viz_id + '_viz_frame_div');
        var model_sel = $('#co2_emissions_model_name');
        var model_full = (model_sel.multipleSelect('getSelects').length === 0);
        if (model_full) {
            alert('Please, select at least one value from each field to update the visualisation.')
        } else {
            viz_frame.show();
            token_retrieval();

            /* # Query creation*/
            var jq_obj = create_co2_emissions_query(dataset);
            console.log(viz_id + ' - JSON Query Created');
            retrieve_series_info_summary(jq_obj, dataset, viz_id, viz_type, intrfc,false,["moody_blue", "light_red", "cyan", "orange_fire", "grey_green", "light_brown", "gold", "ice_gray" ,"purple"],[],[],[],String(jq_obj["variables"]));

        }
    });



    function create_co2_emissions_query(dataset) {
        var sel_model = $('#co2_emissions_model_name');
        var variable = ['Emissions|CO2|Energy'];
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


    $("#co2_emissions-run-button").trigger('click');
});

