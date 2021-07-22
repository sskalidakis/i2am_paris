$(document).ready(function () {

    function run_hydrogen_production_by_fuel() {
        var viz_frame = $('#hydrogen_production_by_fuel_viz_frame_div');
        viz_frame.show();
        /* Token Retrieval*/
        const csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        });
        /* # Query creation*/
        var jq_obj = create_hydrogen_production_by_fuel_query();
        console.log(jq_obj);
        console.log('hydrogen_production_by_fuel JSON Query Created');
        start_qc_v_hydrogen_production_by_fuel_process(jq_obj);


    };

    function start_qc_v_hydrogen_production_by_fuel_process(json_query_obj) {
        var query = {};
        query["query_name"] = "wwheu_pub_hydrogen_production_by_fuel_query";
        query["parameters"] = json_query_obj['query_data'];
        $.ajax({
            url: "/data_manager/create_query",
            type: "POST",
            data: JSON.stringify(query),
            contentType: 'application/json',
            success: function (data) {
                console.log('hydrogen_production_by_fuel Query Saved in DB');
                var query_id = data['query_id'];
                create_visualisation_hydrogen_production_by_fuel(query_id);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }


    function create_visualisation_hydrogen_production_by_fuel(query_id) {
        var viz_frame = $('#hydrogen_production_by_fuel_viz_iframe');
        viz_frame.off();
        viz_frame.hide();
        $('#hydrogen_production_by_fuel_loading_bar').show();

        var data = {
            "y_var_names": ['EU-TIMES_Secondary Energy|Hydrogen|Biomass|w/ CCS', 'EU-TIMES_Secondary Energy|Hydrogen|Fossil|w/ CCS', 'EU-TIMES_Secondary Energy|Hydrogen|Biomass|w/o CCS', 'EU-TIMES_Secondary Energy|Hydrogen|Electricity', 'EU-TIMES_Secondary Energy|Hydrogen|Fossil|w/o CCS', 'GCAM_Secondary Energy|Hydrogen|Biomass|w/ CCS', 'GCAM_Secondary Energy|Hydrogen|Fossil|w/ CCS', 'GCAM_Secondary Energy|Hydrogen|Biomass|w/o CCS', 'GCAM_Secondary Energy|Hydrogen|Electricity', 'GCAM_Secondary Energy|Hydrogen|Fossil|w/o CCS', 'TIAM_Secondary Energy|Hydrogen|Biomass|w/ CCS', 'TIAM_Secondary Energy|Hydrogen|Fossil|w/ CCS', 'TIAM_Secondary Energy|Hydrogen|Biomass|w/o CCS', 'TIAM_Secondary Energy|Hydrogen|Electricity', 'TIAM_Secondary Energy|Hydrogen|Fossil|w/o CCS'],
            "y_var_titles": ['Secondary Energy|Hydrogen|Biomass|w/ CCS', 'Secondary Energy|Hydrogen|Fossil|w/ CCS', 'Secondary Energy|Hydrogen|Biomass|w/o CCS', 'Secondary Energy|Hydrogen|Electricity', 'Secondary Energy|Hydrogen|Fossil|w/o CCS', 'Secondary Energy|Hydrogen|Biomass|w/ CCS', 'Secondary Energy|Hydrogen|Fossil|w/ CCS', 'Secondary Energy|Hydrogen|Biomass|w/o CCS', 'Secondary Energy|Hydrogen|Electricity', 'Secondary Energy|Hydrogen|Fossil|w/o CCS', 'Secondary Energy|Hydrogen|Biomass|w/ CCS', 'Secondary Energy|Hydrogen|Fossil|w/ CCS', 'Secondary Energy|Hydrogen|Biomass|w/o CCS', 'Secondary Energy|Hydrogen|Electricity', 'Secondary Energy|Hydrogen|Fossil|w/o CCS'],
            "y_var_units": ['EJ/yr'],
            "y_axis_title": 'Hydrogen Production',
            "x_axis_name": "year",
            "x_axis_title": "Year",
            "x_axis_unit": "-",
            "x_axis_type": "text",
            "cat_axis_names": ['eu_times', 'gcam', 'tiam'],
            "cat_axis_titles": ['EU-TIMES', 'GCAM', 'TIAM'],
            "use_default_colors": false,
            "color_list_request": ["casual_green", "grey_green", "moody_blue", "blue", "dark_gray"],
            "dataset": query_id,
            "dataset_type": "query",
            "type": "step_by_step"
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
        console.log('hydrogen_production_by_fuel Ready to launch visualisation');
        var complete_url = "/visualiser/show_stacked_clustered_column_chart?" + url;
        viz_frame.attr('src', complete_url);
        viz_frame.on('load', function () {
            console.log('hydrogen_production_by_fuel Visualisation Completed');
            $(this).show();
            $.ajax({
                url: "/data_manager/delete_query",
                type: "POST",
                data: JSON.stringify(query_id),
                contentType: 'application/json',
                success: function (data) {
                    console.log("Chydrogen_production_by_fuel Temporary Query Deleted");
                },
                error: function (data) {
                    console.log(data);
                }
            });

            $('#hydrogen_production_by_fuel_loading_bar').hide();

        });

    }

    function create_hydrogen_production_by_fuel_query() {
        var regions = ['EU'];
        var models = ['eu_times', 'gcam', 'tiam'];
        var variables = ['Secondary Energy|Hydrogen|Biomass|w/ CCS', 'Secondary Energy|Hydrogen|Fossil|w/ CCS', 'Secondary Energy|Hydrogen|Biomass|w/o CCS', 'Secondary Energy|Hydrogen|Electricity', 'Secondary Energy|Hydrogen|Fossil|w/o CCS'];
        var agg_func = 'Avg';
        var agg_var = 'model_id';

        const input_dict = {
            'model__name': models,
            'region__name': regions,
            'variable__name': variables
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
                "ordering": [
                    {
                        "parameter": "model__name",
                        "ascending": true
                    },
                    {
                        "parameter": "year",
                        "ascending": true
                    }
                ]
                ,
                "grouping": {
                    "params": [agg_var, "variable__name", "year", "region__name"],
                    "aggregated_params": [{"name": "value", "agg_func": agg_func}]
                },

            },
            "additional_app_parameters": {}

        };

        return {
            "models": models,
            "variables": variables,
            "regions": regions,
            "query_data": query_data
        }

    }

    run_hydrogen_production_by_fuel();




});

