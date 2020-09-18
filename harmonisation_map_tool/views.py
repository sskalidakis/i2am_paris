from django.http import JsonResponse
from django.shortcuts import render
import json

from i2amparis_main import countries_data
from i2amparis_main.models import ModelsInfo, Harmonisation_Variables, HarmData


def request_harmonisation_data(request):
    if request.method == "POST":
        requested_models = json.loads(request.body)
        models = ModelsInfo.objects.all().filter(model_name__in=requested_models).order_by('model_title')
        model_list = []
        for model in models:
            dict = {}
            dict['model_name'] = model.model_name
            dict['model_title'] = model.model_title
            model_list.append(dict)
        context = {"selected_models": model_list}
        return JsonResponse(context)


def harmonisation_manual(request):
    db = countries_data.RetriveDB('')
    data = db.create_json()
    list_of_models = db.create_models_btn()
    models = ModelsInfo.objects.all().order_by('model_title')
    variables = Harmonisation_Variables.objects.all().order_by('var_title')
    context = {"models": models,
               "variables": variables,
               "buttons": list_of_models
               }

    return render(request, 'harmonisation_map_tool/harmonisation_manual.html', context)