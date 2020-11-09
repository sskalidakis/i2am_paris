function getselects(model_sel, scenario_sel, region_sel, variable_sel) {

    const models = model_sel.multipleSelect('getSelects');
    const scenarios = scenario_sel.multipleSelect('getSelects');
    const regions = region_sel.multipleSelect('getSelects');
    const variables = variable_sel.multipleSelect('getSelects');

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
            },
            error: function (data) {
                console.log(data);
            }
        });
   }