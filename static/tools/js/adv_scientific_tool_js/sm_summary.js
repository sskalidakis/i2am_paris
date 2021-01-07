$(document).ready(function () {
    setTimeout(function () {
        $("#clear-button_intro_comp").click();
    }, 10);

    $('select.boot-select-intro').each(function () {
        var select = $(this);
        select.multipleSelect(
            {
                filter: true,
                showClear: true,
                animate: 'fade',
                maxHeightUnit: 'row',
                maxHeight: 8,
                dropWidth: 250//,
                // onClick: function () {
                //     update_unavailable_select_options(select.attr('id'));
                //     populate_selects('#' + select.attr('id'));
                // },
                // onCheckAll: function () {
                //     update_unavailable_select_options(select.attr('id'));
                //     populate_selects('#' + select.attr('id'));
                // },
                // onUncheckAll: function () {
                //     update_unavailable_select_options(select.attr('id'));
                //     populate_selects('#' + select.attr('id'));
                // },
            });
    });


});

$("#clear-button_intro_comp").click(function () {
    $('select.boot-select-intro').multipleSelect('setSelects', []);
    $('#viz_frame_div_intro_comp').hide();
    $('#chart-side-info_intro_comp').show();
});


$("#run-button_sm_intro_comp").click(function () {
    var viz_frame = $('#viz_frame_div_intro_comp');
    var chart_info = $('#chart-side-info_intro_comp');
    var model_sel = $('#model_name_intro_comp');
    var scenario_sel = $('#scenario_name_intro_comp');
    var variable_sel = $('#variable_name_intro_comp');


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

    query["parameters"] = json_query_obj['data'];

    //var variable_selection = (variable_sel.multipleSelect('getSelects', 'text'));
    const variable_selection = "Year";
    $.ajax({
        url: "/data_manager/create_query",
        type: "POST",

        data: JSON.stringify(query),
        contentType: 'application/json',
        success: function (data) {
            console.log("query created");
            $('.viz-container').show();
            var query_id = data['query_id'];
            create_visualisation_col(query_id, json_query_obj['val_list'], json_query_obj['title_list'], json_query_obj['unit_list'], json_query_obj['grouping_var'], json_query_obj['grouping_var_title'], variable_selection);
        }, //CREATE NEW FUNCTION THAT CALL COLUMN CHART QUERY
        error: function (data) {
            console.log(data);
        }
    });

});

// $('#viz_frame_div_intro_comp iframe').contents().find('body').click(function () {
//     $('select.boot-select').multipleSelect('close');
// });

