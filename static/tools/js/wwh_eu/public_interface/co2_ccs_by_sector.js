$(document).ready(function () {


    $('select.model-select').multipleSelect('destroy').multipleSelect(
        {
            filter: true,
            showClear: false,
            animate: 'fade',
            maxHeightUnit: 'row',
            maxHeight: 8,
            dropWidth: 250,
            selectAll: false,
            placeholder: 'Please select a value',
            onClick: function () {
                run_co2_ccs_by_sector();
            },

        });

    function run_co2_ccs_by_sector() {
        const models = $('#model_select').multipleSelect('getSelects');
        var viz_frame = $('#co2_ccs_by_sector_viz_frame_div');
        viz_frame.show();
        /* Token Retrieval*/
        const csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        });
        /* # Query creation*/
        var jq_obj = create_co2_ccs_by_sector_query(models);
        console.log(jq_obj);
        console.log('co2_ccs_by_sector JSON Query Created');
        start_qc_v_co2_ccs_by_sector_process(jq_obj);


    };

    function start_qc_v_co2_ccs_by_sector_process(json_query_obj) {
        var query = {};
        query["query_name"] = "wwheu_pub_co2_ccs_by_sector_query";
        query["parameters"] = json_query_obj['query_data'];
        $.ajax({
            url: "/data_manager/create_query",
            type: "POST",
            data: JSON.stringify(query),
            contentType: 'application/json',
            success: function (data) {
                console.log('co2_ccs_by_sector Query Saved in DB');
                var query_id = data['query_id'];
                create_visualisation_co2_ccs_by_sector(query_id);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }


    function create_visualisation_co2_ccs_by_sector(query_id) {
        var viz_frame = $('#co2_ccs_by_sector_viz_iframe');
        viz_frame.off();
        viz_frame.hide();
        $('#co2_ccs_by_sector_loading_bar').show();

        var data = {
            "y_var_names": ['Carbon Sequestration|CCS|Industrial Processes', 'Carbon Sequestration|CCS|Energy|Supply|Hydrogen', 'Carbon Sequestration|CCS|Energy|Supply', 'Carbon Sequestration|CCS|Energy|Supply|Other'],
            "y_var_titles": ['Carbon Sequestration|CCS|Industrial Processes', 'Carbon Sequestration|CCS|Energy|Supply|Hydrogen', 'Carbon Sequestration|CCS|Energy|Supply', 'Carbon Sequestration|CCS|Energy|Supply|Other'],
            "y_var_units": ['Mt CO2/y', 'Mt CO2/y'],
            "y_axes_titles": ['CO2 Captured','CO2 Emissions'],
            "x_axis_name": "year",
            "x_axis_title": "Year",
            "x_axis_unit": "-",
            "x_axis_type": "text",
            "line_names": ['Emissions|CO2'],
            "line_titles": ['Emissions|CO2'],
            "use_default_colors": false,
            "color_list_request": ["moody_blue", "dark_blue", "violet", "light_red", "ceramic", "orange_yellow", "grey_green", "cyan", "black"],
            "dataset": query_id,
            "dataset_type": "query"
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
        console.log('co2_ccs_by_sector Ready to launch visualisation');
        var complete_url = "/visualiser/show_stacked_column_line_chart?" + url;
        viz_frame.attr('src', complete_url);
        viz_frame.on('load', function () {
            console.log('co2_ccs_by_sector Visualisation Completed');
            $(this).show();
            $.ajax({
                url: "/data_manager/delete_query",
                type: "POST",
                data: JSON.stringify(query_id),
                contentType: 'application/json',
                success: function (data) {
                    console.log("co2_ccs_by_sector Temporary Query Deleted");
                },
                error: function (data) {
                    console.log(data);
                }
            });

            $('#co2_ccs_by_sector_loading_bar').hide();

        });

    }

    function create_co2_ccs_by_sector_query(sel_models) {
        var regions = ['EU'];
        var scenarios = ['PR_CurPol_CP', 'PR_WWH_CP'];
        var models = sel_models;
        var variables = ['Emissions|CO2', 'Carbon Sequestration|CCS|Industrial Processes', 'Carbon Sequestration|CCS|Energy|Supply|Hydrogen', 'Carbon Sequestration|CCS|Energy|Supply', 'Carbon Sequestration|CCS|Energy|Supply|Other'];

        const input_dict = {
            'model__name': models,
            'region__name': regions,
            'variable__name': variables,
            'scenario__name': scenarios
        };
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

            and_dict.push({
                'operand_1': selected[j],
                'operand_2': temp,
                'operation': 'in'
            });
        }


        selected.push('value', 'year');
        const query_data = {
            "dataset": "i2amparis_main_wwheuresultscomp",
            "query_configuration": {
                "select": selected,
                "filter": {
                    "and": and_dict,
                    "or": or_dict
                },
                "ordering": [                    {
                        "parameter": "year",
                        "ascending": true
                    }
                ]
                ,
                "grouping": {"params": [], "aggregated_params": []},

            },
            "additional_app_parameters": {}

        };

        return {
            "models": models,
            "variables": variables,
            "regions": regions,
            "scenarios":scenarios,
            "query_data": query_data
        }

    }

    run_co2_ccs_by_sector();


});

