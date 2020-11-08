function getselects() {
    var sel_model = $('#model_name');
    var sel_scenario = $('#scenario_name');
    var sel_region = $('#region_name');
    var sel_variable = $('#variable_name');

    const models = sel_model.multipleSelect('getSelects');
    const scenarios = sel_scenario.multipleSelect('getSelects');
    const regions = sel_region.multipleSelect('getSelects');
    const variables = sel_variable.multipleSelect('getSelects');
    console.log("hello")
    console.log(models)
    const d = {'model__name': models, 'scenario__name': scenarios, 'region__name': regions, 'variable__name': variables};
    $.ajax({
            url: "/getselectview",
            type: "POST",
            data: JSON.stringify(d),
            contentType: 'application/json',
            success: function (data) {
                console.log("query created");
                console.log(data);

                $('#example').DataTable({
                    "data": data,
                    columns: [
                        {"data": "year"},
                        {"data": "value"},
                        {"data": "region"},
                        {"data": "scenario"},
                        {"data": "unit"},
                        {"data": "variable"},
                        {"data": "model"}
                    ]
                });
                //var query_id = data['query_id'];
            },
            error: function (data) {
                console.log(data);
            }
        });
   }