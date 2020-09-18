import json

from django.http import JsonResponse

from data_manager.models import Query



def heatmap_query(query_id):
    query_name = Query.objects.get(id=query_id).query_name
    if query_name == 'var_harmonisation_on_demand':
        results = var_harmonisation_on_demand(query_id)
        return results


def var_harmonisation_on_demand(query_id):
    from i2amparis_main.models import HarmData
    json_params = get_query_parameters(query_id)
    model_list = []
    if 'model_list' in json_params.keys():
        model_list = json_params['model_list']
    results = HarmData.objects.filter(model__model_name__in=model_list)
    var_mod = []
    for el in results:
        dict_el = {
            "model": el.model.model_title,
            "var": el.variable.var_title,
            "status":el.io_status,
            "var_unit": el.var_unit,
            "var_source_info": el.var_source_info,
            "var_timespan": el.var_timespan
        }
        var_mod.append(dict_el)

    return var_mod


def get_query_parameters(query_id):
    query = Query.objects.get(id=query_id)
    parameters = query.parameters
    json_params = json.loads(parameters)
    return json_params
