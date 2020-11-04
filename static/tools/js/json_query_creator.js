
function create_query_json() {
    const models = $('#model_name').multipleSelect('getSelects');
    const scenarios = $('#scenario_name').multipleSelect('getSelects');
    const regions = $('#region_name').multipleSelect('getSelects');
    const variables = $('#variable_name').multipleSelect('getSelects');
    const input_dict = {'model': models, 'scenario': scenarios, 'region': regions, 'variable': variables};
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
    const data = {
        "dataset": "dataset_1",
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
            "grouping": {},
        },
        "additional_app_parameters": {}
    };
    console.log(JSON.stringify(data));
    return data;

}



const sendQuery = () => {
    let payload = JSON.stringify({
        data: create_query_json()
    });
    $.ajax({
        type: "POST",
        url: "{%url 'receive_data' %}",
        headers: {'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
        // success: location.reload(),
        data: payload,
        dataType: "json",
    });
}

