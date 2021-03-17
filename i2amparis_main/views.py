from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import countries_data
from django.utils.html import format_html
from i2amparis_main.models import ModelsInfo, Harmonisation_Variables, HarmDataNew, HarmDataSourcesLinks, ScenariosRes, \
    RegionsRes, ResultsComp, VariablesRes, UnitsRes, DataVariablesModels, HarmDataSourcesTitles, PRWMetaData, SdgsCat, \
    VaraiblesSdgsRes
from django.core.mail import send_mail
from .forms import FeedbackForm
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.db.models import Avg, Sum, Max, Min, Count, F

import json
import urllib

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages


def landing_page(request):
    print('Landing page')
    return render(request, 'i2amparis_main/landing_page.html')


def overview_comparative_assessment_doc(request):
    print('Overview Comparative Assessment')
    return render(request, 'i2amparis_main/overview_comparative_assessment_landing_page.html')


def overview_comparative_assessment_doc_global(request):
    print('Overview Comparative Assessment Global')
    return render(request, 'i2amparis_main/overview_comparative_assessment_global.html')


def overview_comparative_assessment_doc_national_eu(request):
    print('Overview Comparative Assessment National EU')
    return render(request, 'i2amparis_main/overview_comparative_assessment_eu.html')


def overview_comparative_assessment_doc_national_oeu(request):
    print('Overview Comparative Assessment National O_EU')
    return render(request, 'i2amparis_main/overview_comparative_assessment_oeu.html')


def paris_reinforce_landing(request):
    context = {}
    return render(request, 'i2amparis_main/paris_workspace_landing.html', context)


def paris_reinforce_harmonisation(request):
    models = ModelsInfo.objects.all().filter(harmonisation=True).order_by('model_title')
    variables = Harmonisation_Variables.objects.all().order_by('order')
    var_mod_data = HarmDataNew.objects.all()
    var_mod = []
    for el in var_mod_data:
        dict_el = {
            "model": el.model.name,
            "var": el.variable.var_name,
            "var_unit": el.var_unit,
            "var_timespan": el.var_timespan,
        }

        temp_sources = HarmDataSourcesLinks.objects.filter(model__name=el.model.name,
                                                           variable__var_name=el.variable.var_name).values(
            "var_source_info", "var_source_url", "title")
        titles = set([i['title'] for i in temp_sources])
        temp_sources_dict = {}
        for title in titles:
            temp_data = list(filter(lambda x: x['title'] == title, temp_sources))
            temp_sources_lst = [{'var_source_url': i['var_source_url'], 'var_source_info': i['var_source_info']} for i
                                in
                                temp_data]
            temp_sources_dict[HarmDataSourcesTitles.objects.get(id=title).title] = temp_sources_lst
        try:

            dict_el['source_info'] = temp_sources_dict
        except:
            dict_el['source_info'] = []
        var_mod.append(dict_el)
    print(var_mod)
    context = {"models": models,
               "variables": variables,
               "var_mod": var_mod}
    return render(request, 'i2amparis_main/paris_reinforce_harmonisation.html', context)


def paris_advanced_scientific_module(request):
    models = DataVariablesModels.objects.filter(name__in=['42', 'e3me', 'gcam', 'gemini_e3', 'ices', 'muse', 'tiam']).order_by('title')
    scenarios = ScenariosRes.objects.all().order_by('title')
    regions = RegionsRes.objects.all().order_by('title')
    variables = VariablesRes.objects.all().order_by('title')
    units = UnitsRes.objects.all().order_by('title')

    context = {"models": models,
               "variables": variables,
               "scenarios": scenarios,
               "regions": regions,
               "units": units}

    return render(request, 'i2amparis_main/paris_workspace_scientific_module.html', context)


@csrf_exempt
def update_scientific_model_selects_strict(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if request.method == 'POST':
        models = body['model__name']
        scenarios = body['scenario__name']
        regions = body['region__name']
        variables = body['variable__name']
        changed_field = body['changed_field']
        fe_all_scenarios = body['fe_all_scenarios']
        fe_all_regions = body['fe_all_regions']
        fe_all_models = body['fe_all_models']

        all_models = [el['name'] for el in DataVariablesModels.objects.filter(
            name__in=['42', 'e3me', 'gcam', 'gemini_e3', 'ices', 'muse', 'tiam']).values('name')]
        all_scenarios = [el['name'] for el in ScenariosRes.objects.values('name')]
        all_regions = [el['name'] for el in RegionsRes.objects.values('name')]
        all_variables = [el['name'] for el in VariablesRes.objects.values('name')]

        if changed_field == 'clear_all':
            allowed_models = all_models
            allowed_scenarios = all_scenarios
            allowed_variables = all_variables
            allowed_regions = all_regions
        elif changed_field == 'variable_name':
            if len(models) == 0:
                allowed_models = all_models
                allowed_scenarios = all_scenarios
                allowed_variables = all_variables
                allowed_regions = all_regions
            else:
                distinct_regions = []
                for variable in variables:
                    distinct_regions.append(
                        PRWMetaData.objects.filter(model_name=variable).values('variable_name').distinct())
                final_regions = distinct_regions[0]
                for regions_list in distinct_regions:
                    final_regions = final_regions.intersection(regions_list)
                print('common regions', final_regions)
                allowed_regions = [el['region_name'] for el in final_regions]
                allowed_models = all_models
                allowed_variables = all_variables
                allowed_scenarios = all_scenarios
        elif changed_field == 'region_name':
            if len(regions) == 0:
                allowed_models = all_models
                allowed_regions = [el for el in all_regions if el not in fe_all_regions]
                allowed_variables = variables
                allowed_scenarios = all_scenarios
            else:
                distinct_scenarios = []
                for variable in variables:
                    for region in regions:
                        distinct_scenarios.append(
                            PRWMetaData.objects.filter(variable_name=variable, region_name=region).values(
                                'scenario_name').distinct())
                final_scenarios = distinct_scenarios[0]
                for scenarios_list in distinct_scenarios:
                    final_scenarios = final_scenarios.intersection(scenarios_list)
                print('common scenarios', final_scenarios)
                allowed_regions = [el for el in all_regions if el not in fe_all_regions]
                allowed_models = all_models
                allowed_variables = variables
                allowed_scenarios = [el['scenario_name'] for el in final_scenarios]
        elif changed_field == 'scenario_name':
            if len(scenarios) == 0:
                allowed_variables = variables
                allowed_regions = regions
                allowed_models = all_models
                allowed_scenarios = [el for el in all_scenarios if el not in fe_all_scenarios]
            else:
                distinct_models = []
                for variable in variables:
                    for region in regions:
                        for scenario in scenarios:
                            distinct_models.append(
                                PRWMetaData.objects.filter(variable_name=variable, scenario_name=scenario,
                                                           region_name=region).values(
                                    'model_name').distinct())
                final_models = distinct_models[0]
                for model_list in distinct_models:
                    final_models = final_models.intersection(model_list)
                print('common models', final_models)
                allowed_variables = variables
                allowed_regions = regions
                allowed_models = [el['model_name'] for el in final_models]
                allowed_scenarios = [el for el in all_scenarios if el not in fe_all_scenarios]
        elif changed_field == 'model_name':

            allowed_variables = variables
            allowed_scenarios = scenarios
            allowed_models = [el for el in all_models if el not in fe_all_models]
            allowed_regions = regions

        ls = {'models': [el for el in all_models if el not in allowed_models],
              'scenarios': [el for el in all_scenarios if el not in allowed_scenarios],
              'regions': [el for el in all_regions if el not in allowed_regions],
              'variables': [el for el in all_variables if el not in allowed_variables]}

        print('Changed field: ', changed_field)

        return JsonResponse(ls, safe=False)



@csrf_exempt
def update_scientific_model_selects_basic(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if request.method == 'POST':
        models = body['model__name']
        scenarios = body['scenario__name']
        regions = body['region__name']
        variables = body['variable__name']
        changed_field = body['changed_field']
        fe_all_scenarios = body['fe_all_scenarios']
        fe_all_regions = body['fe_all_regions']
        fe_all_models = body['fe_all_models']

        all_models = [el['name'] for el in DataVariablesModels.objects.filter(
            name__in=['42', 'e3me', 'gcam', 'gemini_e3', 'ices', 'muse', 'tiam']).values('name')]
        all_scenarios = [el['name'] for el in ScenariosRes.objects.values('name')]
        all_regions = [el['name'] for el in RegionsRes.objects.values('name')]
        all_variables = [el['name'] for el in VariablesRes.objects.values('name')]

        if changed_field == 'clear_all':
            allowed_models = all_models
            allowed_scenarios = all_scenarios
            allowed_variables = all_variables
            allowed_regions = all_regions
        elif changed_field == 'variable_name':
            if len(models) == 0:
                allowed_models = all_models
                allowed_scenarios = all_scenarios
                allowed_variables = all_variables
                allowed_regions = all_regions
            else:
                distinct_regions = []
                for variable in variables:
                    distinct_regions.append(
                        PRWMetaData.objects.filter(model_name=variable).values('variable_name').distinct())
                final_regions = distinct_regions[0]
                for regions_list in distinct_regions:
                    final_regions = (final_regions | regions_list).distinct()
                print('common regions', final_regions)
                allowed_regions = [el['region_name'] for el in final_regions]
                allowed_models = all_models
                allowed_variables = all_variables
                allowed_scenarios = all_scenarios
        elif changed_field == 'region_name':
            if len(regions) == 0:
                allowed_models = all_models
                allowed_regions = [el for el in all_regions if el not in fe_all_regions]
                allowed_variables = variables
                allowed_scenarios = all_scenarios
            else:
                distinct_scenarios = []
                for variable in variables:
                    for region in regions:
                        distinct_scenarios.append(
                            PRWMetaData.objects.filter(variable_name=variable, region_name=region).values(
                                'scenario_name').distinct())
                final_scenarios = distinct_scenarios[0]
                for scenarios_list in distinct_scenarios:
                    final_scenarios = (final_scenarios | scenarios_list).distinct()
                print('common scenarios', final_scenarios)
                allowed_regions = [el for el in all_regions if el not in fe_all_regions]
                allowed_models = all_models
                allowed_variables = variables
                allowed_scenarios = [el['scenario_name'] for el in final_scenarios]
        elif changed_field == 'scenario_name':
            if len(scenarios) == 0:
                allowed_variables = variables
                allowed_regions = regions
                allowed_models = all_models
                allowed_scenarios = [el for el in all_scenarios if el not in fe_all_scenarios]
            else:
                distinct_models = []
                for variable in variables:
                    for region in regions:
                        for scenario in scenarios:
                            distinct_models.append(
                                PRWMetaData.objects.filter(variable_name=variable, scenario_name=scenario,
                                                           region_name=region).values(
                                    'model_name').distinct())
                final_models = distinct_models[0]
                for model_list in distinct_models:
                    final_models = (final_models | model_list).distinct()
                print('common models', final_models)
                allowed_variables = variables
                allowed_regions = regions
                allowed_models = [el['model_name'] for el in final_models]
                allowed_scenarios = [el for el in all_scenarios if el not in fe_all_scenarios]
        elif changed_field == 'model_name':

            allowed_variables = variables
            allowed_scenarios = scenarios
            allowed_models = [el for el in all_models if el not in fe_all_models]
            allowed_regions = regions


        ls = {'models': [el for el in all_models if el not in allowed_models],
              'scenarios': [el for el in all_scenarios if el not in allowed_scenarios],
              'regions': [el for el in all_regions if el not in allowed_regions],
              'variables': [el for el in all_variables if el not in allowed_variables]}

        print('Changed field: ', changed_field)

        return JsonResponse(ls, safe=False)




@csrf_exempt
def populate_detailed_analysis_datatables(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if request.method == 'POST':
        models = body['model__name']
        scenarios = body['scenario__name']
        regions = body['region__name']
        variables = body['variable__name']

        q = ResultsComp.objects.filter(model__name__in=models, scenario__name__in=scenarios, region__name__in=regions,
                                       variable__name__in=variables)

        ls = []
        for item in q:
            temp = {
                "year": item.year,
                "value": item.value,
                "region": item.region.title,
                "scenario": item.scenario.title,
                "unit": item.unit.name,
                "variable": item.variable.title,
                "model": item.model.title
            }
            ls.append(temp)
        return JsonResponse(ls, safe=False)


def get_sdg_variables(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    ls = []
    if request.method == 'POST':
        sdg = body['sdg_name']
        variables = VaraiblesSdgsRes.objects.filter(sdg__sdgs_cat=sdg)
        for var in variables:
            ls.append({'variable_name': var.variable.name, "variable_title": var.variable.title})
    return JsonResponse(ls, safe=False)





def detailed_model_doc(request, model=''):
    if model == '':
        print('Detailed Model Documentation')
        list_of_models = ModelsInfo.objects.all()
        sel_icons = 'rev_icons'
        context = {
            'model_list': list_of_models,
            'sel_icons': sel_icons
        }
        return render(request, 'i2amparis_main/detailed_model_documentation_landing_page.html', context)
    else:
        category = ModelsInfo.objects.get(model_name=model).coverage
        list_of_cat_models = ModelsInfo.objects.filter(coverage=category)
        print(category)
        print(list_of_cat_models)
        model_dict = []
        for el in list_of_cat_models:
            model_obj = {}
            model_obj['name'] = el.model_name
            model_obj['title'] = el.model_title
            model_obj['harmonisation'] = el.harmonisation
            model_dict.append(model_obj)
        print(model_dict)
        if category == 'global':
            menu_cat = 'Other Global Models'
        elif category == 'national_eu':
            menu_cat = 'Other National / Regional Models for Europe'
        else:
            menu_cat = 'Other National / Regional Models for countries outside Europe'

        return render(request, 'i2amparis_main/detailed_' + model + '.html',
                      context={'menu_models': model_dict, 'coverage': menu_cat})


def dynamic_doc(request, model=''):
    template_format = request.GET.get('format')
    db = countries_data.RetriveDB(model)
    data = db.create_json()
    list_of_models = db.create_models_btn()
    sel_model_long_description = ModelsInfo.objects.get(id=db.model_id).long_description
    print(db.retrieve_granularity)
    sel_icons = 'rev_icons'
    context = {
        'data': data,
        'buttons': list_of_models,
        'granularities': db.retrieve_granularity,
        'selected_model_name': ModelsInfo.objects.get(id=db.model_id).model_name,
        'selected_model_title': ModelsInfo.objects.get(id=db.model_id).model_title,
        'selected_model_description': sel_model_long_description,
        'template_format': template_format,
        'sel_icons': sel_icons
    }
    if template_format is not None:
        template = 'i2amparis_main/dynamic_documentation_final' + template_format + '.html'
    else:
        template = 'i2amparis_main/dynamic_documentation_final.html'
    return render(request, template, context)


def contact_form(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # This can be used to send an email to inform us about the newly submitted feedback.
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email_text = str(username) + ' submitted his/her feedback on I2AM Paris Platform:' + \
                         '\nSubject: "' + str(subject) + '"\nMessage: ' + str(message) + '"\n\n Contact e-mail: ' + str(
                email)

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'

            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                form.save()
                messages.success(request, 'New comment added with success!')
                send_mail(str(username) + "'s Feedback on I2AM Paris Platform", email_text, 'noreply@epu.ntua.gr',
                          ['iam@paris-reinforce.eu', 'paris.reinforce@gmail.com'],
                          fail_silently=False)
                return JsonResponse({'status': 'OK'})
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return JsonResponse({'status': 'NOT_OK'})
