$(document).ready(function () {
    setTimeout(function () {
        $("#clear-button").click();
    }, 10);

});

$("#clear-button").click(function () {
    $('select.boot-select').multipleSelect('setSelects', []);
    $('#viz_frame_div').hide();
    $('#chart_info').show();
});


$("#run-button_sm").click(function () {
    var viz_frame = $('#viz_frame_div_sm');
    var chart_info = $('#chart-side-info_intro_comp');
    var model_sel = $('#model_name_sm');
    var scenario_sel = $('#scenario_name_sm');
    //var region_sel = $('#region_name');
    var variable_sel = $('#variable_name');
    console.log(model_sel.multipleSelect('getSelects'));
    console.log(scenario_sel.multipleSelect('getSelects'));
    //console.log(region_sel.multipleSelect('getSelects'));
    console.log(variable_sel.multipleSelect('getSelects'));
    //var model_full = (model_sel.multipleSelect('getSelects').length === 0);
    //var scenario_full = (scenario_sel.multipleSelect('getSelects').length === 0);
    //var region_full = (region_sel.multipleSelect('getSelects').length === 0);
    //var variable_full = (variable_sel.multipleSelect('getSelects').length === 0);

	viz_frame.show();
	chart_info.show();
	/* Token Retrieval */
	const csrftoken = getCookie('csrftoken');
	$.ajaxSetup({
		beforeSend: function (xhr) {
			xhr.setRequestHeader('X-CSRFToken', csrftoken);
		}
	});

	/* Query creation */
	var query = {};
	query["query_name"] = "quantity_comparison_query";
	var json_query_obj = create_query_json_column(); //DELETE REGION IN NEW FILE JS
	console.log("query obj=", json_query_obj)
	query["parameters"] = json_query_obj['data'];
	console.log("query parameters are:",query["parameters"]);
	// create_chart_info_text(json_query_obj);
	var variable_selection = (variable_sel.multipleSelect('getSelects', 'text'));

	$.ajax({
		url: "/data_manager/create_query",
		type: "POST",

		data: JSON.stringify(query),
		contentType: 'application/json',
		success: function (data) {
			console.log("query created");
			console.log(data);
			$('.viz-container').show();
			var query_id = data['query_id'];
			create_visualisation_col(query_id, json_query_obj['val_list'], json_query_obj['title_list'], json_query_obj['unit_list'], variable_selection);
		}, //CREATE NEW FUNCTION THAT CALL COLUMN CHART QUERY
		error: function (data) {
			console.log(data);
		}
	});
	// populate_datatables(model_sel, scenario_sel, [], variable_sel);

});

//Close-down selects when pressing on the iframe

$('#viz_frame_div iframe').contents().find('body').click(function () {
    $('select.boot-select').multipleSelect('close');
});

