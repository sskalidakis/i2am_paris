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
        new_query = Query(query_name=query_info['query_name'], parameters=query_info['parameters'])
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


def datamanager_template(request):
    models_title = list(DataVariablesModels.objects.all().values_list('title', flat=True))
    variables_title = list(VariablesRes.objects.all().values_list('title', flat=True))
    regions_title = list(RegionsRes.objects.all().values_list('title', flat=True))
    scenarios_title = list(ScenariosRes.objects.all().values_list('title', flat=True))
    context = {
                'models_title': models_title,
                'variables_title': variables_title,
                'regions_title': regions_title,
                'scenarios_title': scenarios_title
    }
    return render(request, 'datamanager.html', context)