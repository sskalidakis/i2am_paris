$(document).ready(function () {
    setTimeout(function () {
        $("#clear-button").click();
    }, 10);


    $('select.boot-select').each(function () {
        var select = $(this);
        select.multipleSelect(
            {
                filter: true,
                showClear: true,
                animate: 'fade',
                maxHeightUnit: 'row',
                maxHeight: 8,
                dropWidth: 250,
                onClick: function () {
                    update_unavailable_select_options(select.attr('id'));
                    populate_selects('#' + select.attr('id'));
                },
                onCheckAll: function () {
                    update_unavailable_select_options(select.attr('id'));
                    populate_selects('#' + select.attr('id'));
                },
                onUncheckAll: function () {
                    update_unavailable_select_options(select.attr('id'));
                    populate_selects('#' + select.attr('id'));
                },
            });
    });

    function transform_multiple_select(selector){
        selector.multipleSelect('destroy').multipleSelect(
            {
                filter: true,
                showClear: true,
                animate: 'fade',
                maxHeightUnit: 'row',
                maxHeight: 8,
                dropWidth: 250,
                onClick: function () {
                    update_unavailable_select_options(selector.attr('id'));
                },
                onCheckAll: function () {
                    update_unavailable_select_options(selector.attr('id'));
                },
                onUncheckAll: function () {
                    update_unavailable_select_options(selector.attr('id'));
                },
            }
        );
    }

    function populate_selects(selector) {
        var sel = $(selector);
        var others_sel = $('select.boot-select:not(' + selector + ')');
        var selected = sel.multipleSelect('getSelects');

        if (selected.length >= 2) {
            console.log("Other selectors=", others_sel);
            others_sel.each(function () {
                var oth_sel = $(this);
                console.log("other sel=",oth_sel);
                $(this).removeAttr('multiple');
                console.log("After remove");
                if ($(this).multipleSelect('getSelects').length === 0) {
                    console.log("in if");
                    transform_multiple_select(oth_sel);
                    $(this).multipleSelect('setSelects', []);
                } else {
                    console.log("In transform");
                    transform_multiple_select(oth_sel);
                }
            })

        } else {
            console.log("In update");
            update_others_function(selector);
        }

    }


    function update_others_function(selector) {
        console.log("Updating selectors");
        var others_sel = $('select.mul-select:not(' + selector + ')');
        others_sel.attr('multiple', 'multiple');
        others_sel.multipleSelect('destroy');
        (others_sel).each(function () {
            var other_select = $(this);
            console.log(other_select);
            $(this).multipleSelect(
                {
                    filter: true,
                    showClear: true,
                    animate: 'fade',
                    maxHeightUnit: 'row',
                    maxHeight: 8,
                    dropWidth: 250,
                    onClick: function () {
                        update_unavailable_select_options(other_select.attr('id'));
                        populate_selects('#' + other_select.attr('id'));
                    },
                    onCheckAll: function () {
                        update_unavailable_select_options(other_select.attr('id'));
                        populate_selects('#' + other_select.attr('id'));
                    },
                    onUncheckAll: function () {
                        update_unavailable_select_options(other_select.attr('id'));
                        populate_selects('#' + other_select.attr('id'));
                    },
                });
        });

    }

    function update_unavailable_select_options(changed) {
       // TODO: FIX the bugs in this method to clear the selects correctly
       /* const models = $('#model_name').multipleSelect('getSelects');
        const scenarios = $('#scenario_name').multipleSelect('getSelects');
        const regions = $('#region_name').multipleSelect('getSelects');
        const variables = $('#variable_name').multipleSelect('getSelects');

        const input = {
            'model__name': models,
            'scenario__name': scenarios,
            'region__name': regions,
            'variable__name': variables,
            'changed': changed
        };

        $.ajax({
            url: "/update_scientific_model_selects",
            type: "POST",
            data: JSON.stringify(input),
            contentType: 'application/json',
            success: function (data) {
                $("option").removeAttr('disabled');
                var j;
                for(j = 0; j < data['models'].length; j++){
                    $("#model_name option[value='"+ data['models'][j] + "']").attr('disabled', 'disabled');
                }

                for (j = 0; j < data['scenarios'].length; j++) {
                    $("#scenario_name option[value='" + data['scenarios'][j] + "']").attr('disabled', 'disabled');
                }

                for (j = 0; j < data['regions'].length; j++) {
                    $("#region_name option[value='" + data['regions'][j] + "']").attr('disabled', 'disabled');
                }

                for (j = 0; j < data['variables'].length; j++) {
                    $("#variable_name option[value='" + data['variables'][j] + "']").attr('disabled', 'disabled');
                }

            },
            error: function (data) {
                console.log('Cannot update disabled selects. AJAX Call failed.');
            }
        });*/


    }
});

$("#clear-button").click(function () {
    $('select.boot-select').multipleSelect('setSelects', []);
    $('#viz_frame_div').hide();
    $('#chart_info').show();
});

$("#run-button").click(function () {
    var viz_frame = $('#viz_frame_div');
    var chart_info = $('#chart-side-info');
    var model_sel = $('#model_name');
    var scenario_sel = $('#scenario_name');
    var region_sel = $('#region_name');
    var variable_sel = $('#variable_name');
    console.log(model_sel.multipleSelect('getSelects'));
    console.log(scenario_sel.multipleSelect('getSelects'));
    console.log(region_sel.multipleSelect('getSelects'));
    console.log(variable_sel.multipleSelect('getSelects'));
    var model_full = (model_sel.multipleSelect('getSelects').length === 0);
    var scenario_full = (scenario_sel.multipleSelect('getSelects').length === 0);
    var region_full = (region_sel.multipleSelect('getSelects').length === 0);
    var variable_full = (variable_sel.multipleSelect('getSelects').length === 0);
    if (model_full || scenario_full || region_full || variable_full) {
        alert('Please, select at least one value from each field.')
    } else {
        viz_frame.show();
        chart_info.show();
        /* Token Retrieval*/
        const csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        });

        /* # Query creation*/
        var query = {};
        query["query_name"] = "scientific_tool_query";
        var json_query_obj = create_query_json();
        query["parameters"] = json_query_obj['data'];
        create_chart_info_text(json_query_obj);
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
                create_visualisation(query_id, json_query_obj['val_list'], json_query_obj['title_list'], json_query_obj['unit_list'], variable_selection);
            },
            error: function (data) {
                console.log(data);
            }
        });
        populate_datatables(model_sel, scenario_sel, region_sel, variable_sel);
    }
});



function create_visualisation(query_id, val_list, title_list, unit_list, variable) {
    var viz_frame = $('#viz_iframe');
    viz_frame.off();
    viz_frame.hide();
    $('#loading_bar').show();

    var data = {
        "y_var_names": val_list,
        "y_var_titles": title_list,
        "y_var_units": unit_list,
        "y_axis_title": String(variable),
        "x_axis_name": "year",
        "x_axis_title": "Year",
        "x_axis_unit": "-",
        "x_axis_type": "text",
        "color_list_request": ["moody_blue", "dark_blue", "violet", "light_red", "ceramic", "orange_yellow", "grey_green", "cyan", "black"],
        "distinct": ["Extractable model output", "Harmonisable model input", "No explicit output or input"],
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

    var complete_url = "/visualiser/show_line_chart?" + url;
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
                console.log(data);
            }
        });

        $('#loading_bar').hide();

    });

}

function toTitleCase(str) {
    return str.replace(/(?:^|\s)\w/g, function (match) {
        return match.toUpperCase();
    });
}

function create_chart_info_text(query_obj) {
    $('#updated-chart-info').empty();
    var field_list = ['model', 'scenario', 'region', 'variable'];
    var multiple_field = query_obj['multiple_field'];
    field_list = field_list.filter(e => e !== multiple_field);
    var dynam_text = '';
    for (var j = 0; j < field_list.length; j++) {
        dynam_text = dynam_text + '<div>' + '<h5 style="margin-bottom: 0.4em; font-weight: 600">' + toTitleCase(field_list[j]) + "</h5>" + "<p style=\"margin-bottom: 0.7em;font-size: 0.9em\">" + String($('#' + field_list[j] + '_name').multipleSelect('getSelects', 'text')[0]) + '</p></div>';
    }
    dynam_text = dynam_text + '<h5 style="margin-bottom: 0.4em">' + toTitleCase(multiple_field) + 's </h5> <ul style="font-size:0.9em">';
    var multiple_values = $('#' + multiple_field + '_name').multipleSelect('getSelects', 'text');
    for (j = 0; j < multiple_values.length; j++) {
        dynam_text = dynam_text + '<li>' + multiple_values[j] + '</li>'
    }
    dynam_text = dynam_text + '</ul>'
    $(dynam_text).appendTo('#updated-chart-info');

}

//Close-down selects when pressing on the iframe

$('#viz_frame_div iframe').contents().find('body').click(function () {
    $('select.boot-select').multipleSelect('close');
});