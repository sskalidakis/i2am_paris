$("#col_order").change(function () {
    var viz_frame = $('#viz_iframe');
    viz_frame.hide();
    $('#loading_bar').show();
    var col_ordering_grouping = $('#col_order option:selected').attr('data-category');
    if ((col_ordering_grouping === "") && (col_ordering_grouping === null) && (col_ordering_grouping === undefined)) {
        col_ordering_grouping = "";
    }
    var data = {
        "row_categorisation_dataset": "datasetvariableharmonisationguides",
        "col_categorisation_dataset": col_ordering_grouping,
        "col_order": $('#col_order').val(),
        "row_order": "order",
        "y_var_names": ["variable"],
        "y_axis_title": "Variables",
        "y_var_units": ["-"],
        "x_axis_name": "model",
        "x_axis_title": "Models",
        "x_axis_unit": "-",
        "z_axis_name": "io_status",
        "z_axis_title": "Value",
        "z_axis_unit": "-",
        "min_max_z_value": 0,
        "color_list_request": ["grey_green", "light_blue", "ice_gray"],
        "distinct": ["Extractable model output", "Harmonisable model input", "No explicit output or input"],
        "dataset": "i2amparis_main_harmdatanew",
        "dataset_type": "db",
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

    var complete_url = "/visualiser/show_heat_map_chart?" + url;
    viz_frame.attr('src', complete_url);
    viz_frame.load(function () {
        $(this).show();

        $('#loading_bar').hide();
        $(this).contents().on('click', function () {

            var col_option = $('iframe').contents().find('#col_clicked').text();
            var col_val = $('#model_name option')
                .filter(function () {
                    return $.trim($(this).text()) === col_option;
                }).val();
            $('#model_name').val(col_val);
            $('#model_name').trigger('change');
            var row_option = $('iframe').contents().find('#row_clicked').text();
            var row_val = $('#var_name option')
                .filter(function () {
                    return $.trim($(this).text()) === row_option;
                }).val();
            $('#var_name').val(row_val);
            $('#var_name').trigger('change');
        })
    });


});
$('#col_order').val('default').trigger('change');


var sel_model_name = $("#model_name");
var sel_geo_cov = $('#geo_cov');
var sel_model_type = $('#model_type');
var sel_model_timestep = $('#model_timestep');
var sel_model_desc = $('#model_desc');
var sel_model_dynamic = $('#model_dynamic');
var sel_var_mod_unit = $('#var_mod_unit');
var sel_var_mod_source = $('#var_mod_source');
var sel_var_mod_timespan = $('#var_mod_timespan');
var sel_var_name = $("#var_name");
var sel_var_def = $('#var_def');
var sel_var_cat = $('#var_cat');
var sel_unit_container = $('.unit_container');
var sel_source_container = $('.source_container');
var sel_timespan_container = $('.timespan_container');

function show_hide_empty_fields() {
    if (sel_var_mod_unit.text() === '') {
        sel_unit_container.hide();
    } else {
        sel_unit_container.show();
    }
    if (sel_var_mod_source.text() === '') {
        sel_source_container.hide();
    } else {
        sel_source_container.show();
    }
    if (sel_var_mod_timespan.text() === '') {
        sel_timespan_container.hide();
    } else {
        sel_timespan_container.show();
    }
}

sel_model_name.change(function () {
    sel_geo_cov.text($('#' + String($(this).val()) + ' .d_model_coverage').text());
    sel_model_type.text($('#' + String($(this).val()) + ' .d_model_type').text());
    sel_model_timestep.text($('#' + String($(this).val()) + ' .d_model_timestep').text());
    sel_model_desc.attr('href', '/detailed_model_doc/' + String($(this).val()));
    sel_model_dynamic.attr('href', '/dynamic_doc/' + String($('#model_name').val()));
    sel_model_desc.html("<i class=\"fa fa-book\"></i> Detailed Documentation of " + String($(this).find('option:selected').text()));
    sel_model_dynamic.html("<i class=\"fa fa-search\"></i> Dynamic Documentation of " + String($(this).find('option:selected').text()));
    sel_var_mod_unit.text($('#' + String(sel_model_name.val()) + '_' + String(sel_var_name.val()) + ' .d_var_mod_unit').text());
    sel_var_mod_source.text($('#' + String(sel_model_name.val()) + '_' + String(sel_var_name.val()) + ' .d_var_mod_source_info').text());
    sel_var_mod_timespan.text($('#' + String(sel_model_name.val()) + '_' + String(sel_var_name.val()) + ' .d_var_mod_timespan').text());
    show_hide_empty_fields();
});
sel_var_name.change(function () {
    sel_var_def.text($('#' + String($(this).val()) + ' .d_var_definition').text());
    sel_var_cat.text($('#' + String($(this).val()) + ' .d_var_category').text());
    sel_var_mod_unit.text($('#' + String(sel_model_name.val()) + '_' + String(sel_var_name.val()) + ' .d_var_mod_unit').text());
    sel_var_mod_source.text($('#' + String(sel_model_name.val()) + '_' + String(sel_var_name.val()) + ' .d_var_mod_source_info').text());
    sel_var_mod_timespan.text($('#' + String(sel_model_name.val()) + '_' + String(sel_var_name.val()) + ' .d_var_mod_timespan').text());
    show_hide_empty_fields();

});
sel_model_desc.attr('href', '/detailed_model_doc/' + String(sel_model_name.val()));
sel_geo_cov.text($('#' + String(sel_model_name.val()) + ' .d_model_coverage').text());
sel_model_type.text($('#' + String(sel_model_name.val()) + ' .d_model_type').text());
sel_model_timestep.text($('#' + String(sel_model_name.val()) + ' .d_model_timestep').text());
sel_model_dynamic.attr('href', '/dynamic_doc/' + String(sel_model_name.val()));
sel_model_desc.html("<i class=\"fa fa-book\"></i> Detailed Documentation of " + String(sel_model_name.find('option:selected').text()));
sel_model_dynamic.html("<i class=\"fa fa-search\"></i> Dynamic Documentation of " + String(sel_model_name.find('option:selected').text()));
sel_var_def.text($('#' + String(sel_var_name.val()) + ' .d_var_definition').text());
sel_var_cat.text($('#' + String(sel_var_name.val()) + ' .d_var_category').text());
show_hide_empty_fields();
