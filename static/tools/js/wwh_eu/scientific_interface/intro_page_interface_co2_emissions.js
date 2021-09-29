$(document).ready(function () {
    $('select.sum-boot-select').each(function () {
        var select = $(this);
        select.multipleSelect(
            {
                filter: true,
                showClear: true,
                animate: 'fade',
                maxHeightUnit: 'row',
                maxHeight: 8,
                dropWidth: 250,
            });
    });

    $("#co2_emissions-clear-button").click(function () {
        $('#co2_emissions select.sum-boot-select').multipleSelect('setSelects', []);
        $('#co2_emissions_viz_frame_div').hide();
    });

    $("#co2_emissions-run-button").click(function () {
        var viz_id = 'co2_emissions';
        var viz_type = 'show_line_chart';
        var intrfc = 'eu_wwh_scientific';
        var viz_frame = $('#' + viz_id + '_viz_frame_div');
        var model_sel = $('#co2_emissions_model_name');
        var scenario_sel = $('#co2_emissions_scenario_name');
        var model_full = (model_sel.multipleSelect('getSelects').length === 0);
        var scenario_full = (scenario_sel.multipleSelect('getSelects').length === 0);
        if (model_full || scenario_full) {
            alert('Please, select at least one value from each field to update the visualisation.')
        } else {
            viz_frame.show();
            token_retrieval();

            /* # Query creation*/
            var jq_obj = create_co2_emissions_query();
            console.log(viz_id + ' - JSON Query Created');
            retrieve_series_info_summary(jq_obj, viz_id, viz_type, intrfc);

        }
    });



    function create_co2_emissions_query() {
        var sel_model = $('#co2_emissions_model_name');
        var sel_scenario = $('#co2_emissions_scenario_name');
        var variable = ['Emissions|CO2|Energy'];

        const models = sel_model.multipleSelect('getSelects');
        const scenarios = sel_scenario.multipleSelect('getSelects');
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

