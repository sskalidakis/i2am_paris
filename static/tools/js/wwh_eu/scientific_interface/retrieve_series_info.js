function retrieve_series_info_summary(jq_obj, viz_id, viz_type, intrfc) {
        const units_info = {
            "model_name": jq_obj["models"],
            "region_name": jq_obj["regions"],
            "scenario_name": jq_obj["scenarios"],
            "variable_name": jq_obj["variables"]
        };
        var instances = [];
        var final_val_list = [];
        var final_title_list = [];
        var final_unit_list = [];
        $.ajax({
            url: "/data_manager/retrieve_series_info_fossil_energy_co2",
            type: "POST",
            data: JSON.stringify(units_info),
            contentType: 'application/json',
            success: function (data) {
                console.log(viz_id + ' - Info Retrieved');
                instances = data["instances"];
                for (var i = 0; i < instances.length; i++) {
                    final_val_list.push(instances[i]['series']);
                    final_title_list.push(instances[i]['title']);
                    final_unit_list.push(instances[i]['unit']);
                }

                var viz_payload = {
                    "y_var_names": final_val_list,
                    "y_var_titles": final_title_list,
                    "y_var_units": final_unit_list,
                    "y_axis_title": String(jq_obj["variables"]),
                    "x_axis_name": "year",
                    "x_axis_title": "Year",
                    "x_axis_unit": "-",
                    "x_axis_type": "text",
                    "color_list_request": ["moody_blue", "dark_blue", "violet", "light_red", "ceramic", "orange_yellow", "grey_green", "cyan", "black"],
                    "dataset_type": "query"
                };
                start_sci_query_creation_viz_execution(jq_obj, viz_id, viz_payload, viz_type, intrfc)

            },
            error: function (data) {
                console.log(data);
            }
        });

    }