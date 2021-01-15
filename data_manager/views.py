from django.http import JsonResponse
from django.shortcuts import render
from data_manager.models import Query
import json
from i2amparis_main.models import *


# Create your views here.

def create_query(request):
    '''
    This API call creates a new query record in the database.
    :param request: Query_name and query configuration parameters are passed in the request body.
    :return:The name and the id of the created query in a JSON Response.
    '''
    if request.method == 'POST':
        query_info = json.loads(request.body)
        new_query = Query(query_name=query_info['query_name'], parameters=json.dumps(query_info['parameters']))
        new_query.save()
        context = {"query_name": new_query.query_name, "query_id": new_query.id}
        return JsonResponse(context)
    else:
        context = {"status": 400,
                   "message": 'This HTTP method is not supported by the API'}
        return JsonResponse(context)


def delete_query(request):
    '''
    This API call is used for deleting a query from the database.
    :param request: The id of the query to be deleted is included in the request body.
    :return: JSON response of whether the call was completed successfully
    '''
    if request.method == 'POST':
        query_id = json.loads(request.body)
        query = Query.objects.get(id=query_id)
        query.delete()
        return JsonResponse({"response": "Successfully deleted query " + str(query_id)})
    else:
        context = {"status": 400,
                   "message": 'This HTTP method is not supported by the API'}
        return JsonResponse(context)


def retrieve_series_info(request):
    if request.method == 'POST':
        unit_info = json.loads(request.body)
        all_regions = [el.name for el in RegionsRes.objects.all()]
        if 'region_name' not in unit_info:
            region_info_temp = all_regions
        else:
            region_info_temp = unit_info['region_name']

        try:
            units = ResultsComp.objects.filter(model__name__in=unit_info['model_name'],
                                               scenario__name__in=unit_info['scenario_name'],
                                               region__name__in=region_info_temp,
                                               variable__name__in=unit_info['variable_name']
                                               ).values(unit_info['multiple'] + '__name',
                                                        unit_info['multiple'] + '__title',
                                                        'unit__name').distinct()
            instances = []
            for obj in units:
                instances.append(
                    {"series": obj[unit_info['multiple'] + '__name'],
                     "title": obj[unit_info['multiple'] + '__title'],
                     "unit": obj['unit__name']}
                )
            context = {"instances": instances}

        except Exception as e:
            print('Cannot retrieve unit for the selected combination')
            print(e)
            context = {}
        print('context: ', context)
        return JsonResponse(context)
    else:
        context = {"status": 400,
                   "message": 'This HTTP method is not supported by the API'}
        return JsonResponse(context)


def retrieve_series_info_fossil_energy_co2(request):
    if request.method == 'POST':
        unit_info = json.loads(request.body)
        try:
            units = ResultsComp.objects.filter(model__name__in=unit_info['model_name'],
                                               scenario__name__in=unit_info['scenario_name'],
                                               variable__name=unit_info['variable_name']
                                               ).values('model__name',
                                                        'model__title',
                                                        'scenario__name',
                                                        'scenario__title',
                                                        'unit__name').distinct()
            instances = []
            for obj in units:
                instances.append(
                    {"series": "{}_{}".format(obj['model__name'], obj['scenario__name']),
                     "title": "{}- {}".format(obj['model__title'], obj['scenario__title']),
                     "unit": obj['unit__name']}
                )
            context = {"instances": instances}

        except Exception as e:
            print('Cannot retrieve unit for the selected combination')
            print(e)
            context = {}
        print('context: ', context)
        return JsonResponse(context)
    else:
        context = {"status": 400,
                   "message": 'This HTTP method is not supported by the API'}
        return JsonResponse(context)


def receive_data(request):
    if request.method == 'POST':
        import json
        from pprint import pprint as pp
        pp(json.loads(request.body))
        context = {"status": 200,
                   "message": 'Success'}
        return JsonResponse(context)
