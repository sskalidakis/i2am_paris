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
    $('#chart-side-info_intro_comp').hide();
});


$("#run-button_sm_intro_comp").click(function () {
    var viz_frame = $('#viz_frame_div_intro_comp');
    var chart_info = $('#chart-side-info_intro_comp');
    var model_sel = $('#model_name_intro_comp');
    var scenario_sel = $('#scenario_name_intro_comp');
    var variable_sel = $('#variable_name_intro_comp');
    var agg_func_sel = $('#agg_func_intro_comp');
    var agg_var = $('input[name="agg_var_input"]:checked');
    var model_full = (model_sel.multipleSelect('getSelects').length === 0);
    var scenario_full = (scenario_sel.multipleSelect('getSelects').length === 0);
    var variable_full = (variable_sel.multipleSelect('getSelects').length === 0);
    var agg_func_full = (agg_func_sel.multipleSelect('getSelects').length === 0);
    if (model_full || scenario_full || variable_full || agg_func_full) {
        alert('Please, fill in the required fields.')
    } else {


        viz_frame.show();
        chart_info.show();
        /* Token Retrieval */
        const csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        });

        /* # Query creation*/
        var jq_obj = create_query_json_column();
        retrieve_series_info_column(model_sel, scenario_sel, variable_sel, agg_var, agg_func_sel, jq_obj);
    }

});

function start_qc_v_column_process(model_sel, scenario_sel, variable_sel, agg_var, agg_func_sel, json_query_obj){
    var query = {};
    query["query_name"] = "quantity_comparison_query";
    query["parameters"] = json_query_obj['data'];
    create_comp_info_text(json_query_obj);
    const variable_selection = variable_sel.multipleSelect('getSelects', 'text')[0];
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
        },
        error: function (data) {
            console.log(data);
        }
    });
    populate_comparative_datatables(model_sel, scenario_sel, variable_sel, agg_var, agg_func_sel);
}

function create_visualisation_col(query_id, val_list, title_list, unit_list, grouping_val, grouping_var_title, variable) {
    var x_unit;
    if (grouping_val === 'year') {
        x_unit = 'year'
    } else {
        x_unit = '-'
    }
    var viz_frame = $('#viz_iframe_intro_comp');
    viz_frame.off();
    viz_frame.hide();
    $('#quantity_loading_bar').show();


    var data = {
        "y_var_names": val_list,
        "y_var_titles": title_list,
        "y_var_units": unit_list,
        "y_axis_title": String(variable),
        "x_axis_name": grouping_val,
        "x_axis_title": grouping_var_title,
        "x_axis_unit": x_unit,
        "x_axis_type": "text",
        "color_list_request": ["moody_blue", "dark_blue", "violet", "light_red", "ceramic", "orange_yellow", "grey_green", "cyan", "black"],
        "dataset": query_id,
        "dataset_type": "query",
    };
    var url = '';
    for (var key in data) {
        if (data.hasOwnProperty(key)) {
            if (Array.isArray(data[key])) {
                for (var j = 0; j < data[key].length; j++) {
                    url = url + String(key) + '[]' + "=" + String(data[key][j]) + '&'
                }
            } else {
                url = url + String(key) + "=" + String(data[key]) + '&'
            }

        }
    }

    var complete_url = "/visualiser/show_column_chart?" + url;
    viz_frame.attr('src', complete_url);
    viz_frame.on('load', function () {
        $(this).show();
        console.log("delete old query");
        $.ajax({
            url: "/data_manager/delete_query",
            type: "POST",
            data: JSON.stringify(query_id),
            contentType: 'application/json',
            success: function (data) {
                console.log(data);
            },
            error: function (data) {
            }
        });

        $('#quantity_loading_bar').hide();

    });

}

const capitalize = (s) => {
    if (typeof s !== 'string') return '';
    return s.charAt(0).toUpperCase() + s.slice(1)
};

function toTitleCase(str) {
    return str.replace(/(?:^|\s)\w/g, function (match) {
        return match.toUpperCase();
    });
}


function create_comp_info_text(query_obj) {

    $('#updated-chart-info_intro_comp').empty();
    var field_list = ['model', 'variable', 'scenario'];
    var multiple_field = query_obj['multiple_field'];
    field_list = field_list.filter(e => e !== multiple_field);
    var dynam_text = '';
    for (var j = 0; j < field_list.length; j++) {
        dynam_text = dynam_text + '<div>' + '<h5 style="margin-bottom: 0.4em; font-weight: 600">' + toTitleCase(field_list[j]) + "</h5>" + "<p style=\"margin-bottom: 0.7em;font-size: 0.9em\">" + String($('#' + field_list[j] + '_name_intro_comp').multipleSelect('getSelects', 'text')[0]) + '</p></div>';
    }
    dynam_text = dynam_text + '<h5 style="margin-bottom: 0.4em">' + toTitleCase(multiple_field) + 's </h5> <ul style="font-size:0.9em">';
    var multiple_values = $('#' + multiple_field + '_name_intro_comp').multipleSelect('getSelects', 'text');
    for (j = 0; j < multiple_values.length; j++) {
        dynam_text = dynam_text + '<li>' + multiple_values[j] + '</li>'
    }
    dynam_text = dynam_text + '</ul>'
    $(dynam_text).appendTo('#updated-chart-info_intro_comp');

}