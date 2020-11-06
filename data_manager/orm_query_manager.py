import json

from django.http import JsonResponse
from django.apps import apps

from data_manager.models import Query
from data_manager.utils import query_execute
from i2amparis_main.models import Dataset
from i2amparis_main.models import ResultsComp
from visualiser.visualiser_settings import DATA_TABLES_APP

def line_chart_query(query_id):
    '''
       This method defines which query is going to be executed for the creation of a line chart
       :param query_id: The query_id of the query to be executed in order to retrieve data for the line chart
       :return: The results of the executed query
       '''
    query_name = Query.objects.get(id=query_id).query_name
    results = []
    if query_name == 'scientific_tool_query':
        results = scentific_tool_query(query_id)
    return results

def heatmap_query(query_id):
    '''
    This method defines which query is going to be executed for the creation of a heatmap chart
    :param query_id: The query_id of the query to be executed in order to retrieve data for the heatmap chart
    :return: The results of the executed query
    '''
    query_name = Query.objects.get(id=query_id).query_name
    if query_name == 'var_harmonisation_on_demand':
        results = var_harmonisation_on_demand(query_id)
        return results


def scentific_tool_query(query_id):
    '''
    This method is the execution of the query for creating data for the advanced scientific tool linechart
    :param query_id: The query_id of the query to be executed in order to retrieve data for the advanced scientific tool linechart
    '''
    app_params = json.loads(Query.objects.get(id=int(query_id)).parameters)
    multiple_field = app_params['additional_app_parameters']['multiple_field']
    # val_list = app_params['additional_app_parameters']['val_list']
    data = query_execute(query_id)
    final_data = []
    temp_year = 0
    temp_dict = {}
    for d in data:
        if temp_year != d['year']:
            if temp_dict != {}:
                final_data.append(temp_dict)
            temp_year = d['year']
            temp_dict = {d[multiple_field + '__name']: d['value'], "year": d['year']}
        else:
            temp_dict[d[multiple_field + '__name']] = d['value']

    return final_data


def var_harmonisation_on_demand(query_id):
    '''
    This method is the execution of the query for creating data for the on-demand variable harmonisation heatmap
    :param query_id: The query_id of the query to be executed in order to retrieve data for the on-demand variable harmonisation heatmap
    :return:
    '''

    from i2amparis_main.models import DatasetOnDemandVariableHarmonisation
    json_params = get_query_parameters(query_id)
    model_list = []
    if 'model_list' in json_params.keys():
        model_list = json_params['model_list']
    # TODO: Create the ordering grouping etc. using the JSON Query format
    results = DatasetOnDemandVariableHarmonisation.objects.filter(model__name__in=model_list).order_by("variable__order")
    var_mod = []
    for el in results:
        dict_el = {
            "model": el.model.title,
            "var": el.variable.var_title,
            "status": el.io_status,
        }
        var_mod.append(dict_el)

    return var_mod


def get_query_parameters(query_id):
    '''
    This method is used for retrieving all the necessary parameters of the query
    :param query_id: The query_id whose parameters are extracted
    :return: A JSON object containing all query parameters
    '''
    query = Query.objects.get(id=query_id)
    parameters = query.parameters
    q_params = json.loads(parameters)
    return q_params