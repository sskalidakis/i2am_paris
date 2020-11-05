$(document).ready(function () {
    $('select').each(function () {
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
                    populate_selects('#' + select.attr('id'))
                },
                onCheckAll: function () {
                    populate_selects('#' + select.attr('id'))
                },
                onUncheckAll: function () {
                    populate_selects('#' + select.attr('id'))
                },
            });
    });


    function populate_selects(selector) {
        var sel = $(selector);
        var others_sel = $('select:not(' + selector + ')');
        var selected = sel.multipleSelect('getSelects');
        if (selected.length >= 2) {
            others_sel.removeAttr('multiple');
            others_sel.multipleSelect('destroy').multipleSelect(
                {
                    filter: true,
                    showClear: true,
                    animate: 'fade',
                    maxHeightUnit: 'row',
                    maxHeight: 8,
                    dropWidth: 250,
                }
            );
        } else {
            update_others_function(selector);
        }


    }


    function update_others_function(selector) {
        var others_sel = $('select.mul-select:not(' + selector + ')');
        others_sel.attr('multiple', 'multiple');
        others_sel.multipleSelect('destroy');
        (others_sel).each(function () {
            var other_select = $(this);
            $(this).multipleSelect(
                {
                    filter: true,
                    showClear: true,
                    animate: 'fade',
                    maxHeightUnit: 'row',
                    maxHeight: 8,
                    dropWidth: 250,
                    onClick: function () {
                        populate_selects('#' + other_select.attr('id'))
                    },
                    onCheckAll: function () {
                        populate_selects('#' + other_select.attr('id'))
                    },
                    onUncheckAll: function () {
                        populate_selects('#' + other_select.attr('id'))
                    },
                });
        });

    }
});

$("#clear-button").click(function () {
    $('select').multipleSelect('setSelects', []);
    $('#viz_frame_div').hide();
});

$("#run-button").click(function () {
    var viz_frame = $('#viz_frame_div');
    var model_sel = $('#model_name');
    var scenario_sel = $('#scenario_name');
    var region_sel = $('#region_name');
    var variable_sel = $('#variable_name');
    var model_full = (model_sel.multipleSelect('getSelects').length === 0);
    var scenario_full = (scenario_sel.multipleSelect('getSelects').length === 0);
    var region_full = (region_sel.multipleSelect('getSelects').length === 0);
    var variable_full = (variable_sel.multipleSelect('getSelects').length === 0);
    if (model_full || scenario_full || region_full || variable_full) {
        alert('Please, select at least one value from each field.')
    } else {
        viz_frame.show();
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