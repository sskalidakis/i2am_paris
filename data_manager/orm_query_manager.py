import json

from django.http import JsonResponse
from django.apps import apps

from data_manager.models import Query
from i2amparis_main.models import Dataset

from visualiser.visualiser_settings import DATA_TABLES_APP

def range_chart_query(query_id):
    from i2amparis_main.models import ResultsComp
    #query_name = Query.objects.get(id=query_id).query_name
    #results = var_harmonisation_on_demand(query_id)
    results = ResultsComp.objects.filter(region_id_id=23, model_id_id=5, scenario_id_id=10, variable_id_id=113).order_by("year")
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


def var_harmonisation_on_demand(query_id):
    '''
    This method is the execution of the query for creating data for the on-demand variable harmonisation heatmap
    :param query_id: The query_id of the query to be executed in order to retrieve data for the on-demand variable harmonisation heatmap
    :return:
    '''
    q_params = get_query_parameters(query_id)
    dataset = q_params['dataset']
    dataset = Dataset.objects.get(dataset_name=dataset)
    data_table = apps.get_model(DATA_TABLES_APP, dataset.dataset_django_model)
    data = data_table.objects.all()
    # variables = Variable.objects.filter(dataset_relation=dataset.id).order_by('id')
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
    json_params = json.loads(parameters)
    return json_params
