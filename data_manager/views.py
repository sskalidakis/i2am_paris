from django.http import JsonResponse
from django.shortcuts import render
from data_manager.models import Query
import json
# Create your views here.

def create_query(request):
    if request.method == 'POST':
        query_info = json.loads(request.body)
        new_query = Query(query_name=query_info['query_name'], parameters=query_info['parameters'])
        new_query.save()
        context = {"query_name": new_query.query_name, "query_id": new_query.id}
        return JsonResponse(context)


def delete_query(request):
    if request.method == 'POST':
        query_name = json.loads(request.body)
        query = Query.objects.get(query_name=query_name)
        query.delete()
        return JsonResponse({"response": "Successfully deleted query " + str(query_name)})