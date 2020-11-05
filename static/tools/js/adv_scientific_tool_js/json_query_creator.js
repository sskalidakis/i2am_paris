
function create_query_json() {
    var sel_model = $('#model_name');
    var sel_scenario = $('#scenario_name');
    var sel_region = $('#region_name');
    var sel_variable = $('#variable_name');

    const models = sel_model.multipleSelect('getSelects');
    const scenarios = sel_scenario.multipleSelect('getSelects');
    const regions = sel_region.multipleSelect('getSelects');
    const variables = sel_variable.multipleSelect('getSelects');

    var multiple_field = "model";
    var val_list = models;
    var title_list = sel_model.multipleSelect('getSelects', 'text');

    $('select').each(function () {
        if ($(this).multipleSelect('getSelects').length > 1) {
            multiple_field = $(this).data('dbname');
            val_list = $(this).multipleSelect('getSelects');
            title_list = $(this).multipleSelect('getSelects', 'text');
        }
    });
    if(val_list.length===0){
        val_list = []
    }

    const input_dict = {'model__name': models, 'scenario__name': scenarios, 'region__name': regions, 'variable__name': variables};
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
        if (temp.length > 1) {
            for (var x in temp) {
                or_dict.push({
                    'operand_1': selected[j],
                    'operand_2': temp[x],
                    'operation': '='
                });
            }
        } else {
            and_dict.push({
                'operand_1': selected[j],
                'operand_2': input_dict[selected[j]][0],
                'operation': '='
            });
        }
    }
    selected.push('value', 'year')
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
                    "parameter": "year",
                    "ascending": true
                },
            ]
            ,
            "grouping": {"params":[], "aggregated_params":[]},
        },
        "additional_app_parameters": {
            "multiple_field": multiple_field,
            "val_list": val_list,
            "title_list": title_list
        }

    };

    //Retrieve units
   return retrieve_series_info(models, regions, scenarios, variables, multiple_field, query_data);

}

function retrieve_series_info(models, regions, scenarios, variables, multiple_field,query_data){
    const units_info = {
        "model_name": models,
        "region_name": regions,
        "scenario_name": scenarios,
        "variable_name": variables,
        "multiple": multiple_field
    };
    var instances = [];
    var final_val_list = [];
    var final_title_list = [];
    var final_unit_list = [];
    $.ajax({
        url: "/data_manager/retrieve_series_info",
        type: "POST",
        data: JSON.stringify(units_info),
        contentType: 'application/json',
        success: function (data) {
            console.log(data);
            instances = data["instances"];
            console.log(JSON.stringify(query_data));
            for (var i = 0; i < instances.length; i++) {
                final_val_list.push(instances[i]['series']);
                final_title_list.push(instances[i]['title']);
                final_unit_list.push(instances[i]['unit']);
            }

        },
        error: function (data) {
            console.log(data);
        }
    });

    return {
        "data": query_data,
        "multiple_field": multiple_field,
        "val_list": final_val_list,
        "title_list": final_title_list,
        "unit_list": final_unit_list
    };

}




