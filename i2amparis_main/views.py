import pdb

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import countries_data
from i2amparis_main.models import ModelsInfo, Harmonisation_Variables, HarmDataNew, HarmDataSourcesLinks, ScenariosRes, \
    RegionsRes, ResultsComp, VariablesRes, UnitsRes, DataVariablesModels, HarmDataSourcesTitles, PRWMetaData, SdgsCat, \
    VaraiblesSdgsRes, RrfPolicy, ProjectModels, PRWEUMetaData, EUHarmData
from django.core.mail import send_mail
from .forms import FeedbackForm
from django.http import JsonResponse, HttpResponse
import os.path


import json
import urllib

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

from .utils import get_initial_detailed_conf_analysis_form_data, create_info_for_var_harmonisation_heatmaps


def landing_page(request):
    print('Landing page')
    return render(request, 'i2amparis_main/landing_page.html')


def overview_comparative_assessment_doc(request):
    print('Overview Comparative Assessment')
    return render(request,
                  'i2amparis_main/overview_comparative_assessment/overview_comparative_assessment_landing_page.html')


def overview_comparative_assessment_doc_global(request):
    print('Overview Comparative Assessment Global')
    return render(request, 'i2amparis_main/overview_comparative_assessment/overview_comparative_assessment_global.html')


def overview_comparative_assessment_doc_national_eu(request):
    print('Overview Comparative Assessment National EU')
    return render(request, 'i2amparis_main/overview_comparative_assessment/overview_comparative_assessment_eu.html')


def overview_comparative_assessment_doc_national_oeu(request):
    print('Overview Comparative Assessment National O_EU')
    return render(request, 'i2amparis_main/overview_comparative_assessment/overview_comparative_assessment_oeu.html')


def paris_reinforce_landing(request):
    context = {}
    return render(request, 'i2amparis_main/paris_reinforce_workspace/paris_workspace_landing.html', context)


def paris_reinforce_harmonisation(request):
    models = ModelsInfo.objects.all().filter(harmonisation=True).order_by('model_title')
    variables = Harmonisation_Variables.objects.all().order_by('order')
    if not os.path.isfile('cached_data/harmonisation_heatmaps/pr_harmonisation_heatmap.json'):
        var_mod_data = HarmDataNew.objects.all()
        harm_data_sources_links = HarmDataSourcesLinks.objects.all()
        var_mod = create_info_for_var_harmonisation_heatmaps(harm_data_sources_links, var_mod_data)
    else:
        print('Heatmap is cached! Loading file...')
        with open('cached_data/harmonisation_heatmaps/pr_harmonisation_heatmap.json') as f:
            data = f.read()
        var_mod = json.loads(data)
    context = {"models": models,
               "variables": variables,
               "var_mod": var_mod}
    return render(request, 'i2amparis_main/paris_reinforce_workspace/paris_reinforce_harmonisation.html', context)



def paris_advanced_scientific_module(request):
    models = DataVariablesModels.objects.filter(
        name__in=['42', 'e3me', 'gcam', 'gemini_e3', 'ices', 'muse', 'tiam']).order_by('title')
    scenarios = ScenariosRes.objects.exclude(name='PR_CurPol_CPO').order_by('title')
    regions = RegionsRes.objects.all().order_by('reg_type')
    filter_vars = PRWMetaData.objects.values('variable_name').distinct()
    var_list = [x['variable_name'] for x in filter_vars]
    variables = VariablesRes.objects.filter(name__in=var_list).order_by('ordering')
    units = UnitsRes.objects.all().order_by('title')

    context = {"models": models,
               "variables": variables,
               "scenarios": scenarios,
               "regions": regions,
               "units": units}

    return render(request, 'i2amparis_main/paris_reinforce_workspace/paris_workspace_scientific_module.html', context)


def paris_cwdtm(request):
    return render(request, 'i2amparis_main/paris_reinforce_workspace/what_does_this_mean.html')


# DEPRECATED NEEDS THE SAME CHANGES WITH BASIC TO BE APPLICABLE TO ANY WORKSPACE
# @csrf_exempt
# def update_scientific_model_selects_strict(request):
#     body_unicode = request.body.decode('utf-8')
#     body = json.loads(body_unicode)
#
#     if request.method == 'POST':
#         models = body['model__name']
#         scenarios = body['scenario__name']
#         regions = body['region__name']
#         variables = body['variable__name']
#         changed_field = body['changed_field']
#         fe_all_scenarios = body['fe_all_scenarios']
#         fe_all_regions = body['fe_all_regions']
#         fe_all_models = body['fe_all_models']
#
#         all_models = [el['name'] for el in DataVariablesModels.objects.filter(
#             name__in=['42', 'e3me', 'gcam', 'gemini_e3', 'ices', 'muse', 'tiam']).values('name')]
#         all_scenarios = [el['name'] for el in ScenariosRes.objects.values('name')]
#         all_regions = [el['name'] for el in RegionsRes.objects.values('name')]
#         all_variables = [el['name'] for el in VariablesRes.objects.values('name')]
#
#         if changed_field == 'clear_all':
#             allowed_models = all_models
#             allowed_scenarios = all_scenarios
#             allowed_variables = all_variables
#             allowed_regions = all_regions
#         elif changed_field == 'variable_name':
#             if len(variables) == 0:
#                 allowed_models = all_models
#                 allowed_scenarios = all_scenarios
#                 allowed_variables = all_variables
#                 allowed_regions = all_regions
#             else:
#                 distinct_regions = []
#                 for variable in variables:
#                     distinct_regions.append(
#                         PRWMetaData.objects.filter(variable_name=variable).values('region_name').distinct())
#                 final_regions = distinct_regions[0]
#                 for regions_list in distinct_regions:
#                     final_regions = final_regions.intersection(regions_list)
#                 print('common regions', final_regions)
#                 allowed_regions = [el['region_name'] for el in final_regions]
#                 allowed_models = all_models
#                 allowed_variables = all_variables
#                 allowed_scenarios = all_scenarios
#         elif changed_field == 'region_name':
#             if len(regions) == 0:
#                 allowed_models = all_models
#                 allowed_regions = [el for el in all_regions if el not in fe_all_regions]
#                 allowed_variables = variables
#                 allowed_scenarios = all_scenarios
#             else:
#                 distinct_scenarios = []
#                 for variable in variables:
#                     for region in regions:
#                         distinct_scenarios.append(
#                             PRWMetaData.objects.filter(variable_name=variable, region_name=region).values(
#                                 'scenario_name').distinct())
#                 final_scenarios = distinct_scenarios[0]
#                 for scenarios_list in distinct_scenarios:
#                     final_scenarios = final_scenarios.intersection(scenarios_list)
#                 print('common scenarios', final_scenarios)
#                 allowed_regions = [el for el in all_regions if el not in fe_all_regions]
#                 allowed_models = all_models
#                 allowed_variables = variables
#                 allowed_scenarios = [el['scenario_name'] for el in final_scenarios]
#         elif changed_field == 'scenario_name':
#             if len(scenarios) == 0:
#                 allowed_variables = variables
#                 allowed_regions = regions
#                 allowed_models = all_models
#                 allowed_scenarios = [el for el in all_scenarios if el not in fe_all_scenarios]
#             else:
#                 distinct_models = []
#                 for variable in variables:
#                     for region in regions:
#                         for scenario in scenarios:
#                             distinct_models.append(
#                                 PRWMetaData.objects.filter(variable_name=variable, scenario_name=scenario,
#                                                            region_name=region).values(
#                                     'model_name').distinct())
#                 final_models = distinct_models[0]
#                 for model_list in distinct_models:
#                     final_models = final_models.intersection(model_list)
#                 print('common models', final_models)
#                 allowed_variables = variables
#                 allowed_regions = regions
#                 allowed_models = [el['model_name'] for el in final_models]
#                 allowed_scenarios = [el for el in all_scenarios if el not in fe_all_scenarios]
#         elif changed_field == 'model_name':
#
#             allowed_variables = variables
#             allowed_scenarios = scenarios
#             allowed_models = [el for el in all_models if el not in fe_all_models]
#             allowed_regions = regions
#
#         ls = {'models': [el for el in all_models if el not in allowed_models],
#               'scenarios': [el for el in all_scenarios if el not in allowed_scenarios],
#               'regions': [el for el in all_regions if el not in allowed_regions],
#               'variables': [el for el in all_variables if el not in allowed_variables]}
#
#         print('Changed field: ', changed_field)
#
#         return JsonResponse(ls, safe=False)


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
        interface = body['interface']

        all_models, all_scenarios, all_regions, all_variables, metadata = get_initial_detailed_conf_analysis_form_data(
            interface)

        if changed_field == 'clear_all':
            allowed_models = all_models
            allowed_scenarios = all_scenarios
            allowed_variables = all_variables
            allowed_regions = all_regions
        elif changed_field == 'variable_name':
            if len(variables) == 0:
                allowed_models = all_models
                allowed_scenarios = all_scenarios
                allowed_variables = all_variables
                allowed_regions = all_regions
            else:
                distinct_regions = []
                for variable in variables:
                    distinct_regions.append(
                        metadata.objects.filter(variable_name=variable).values('region_name').distinct())
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
                            metadata.objects.filter(variable_name=variable, region_name=region).values(
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
                                metadata.objects.filter(variable_name=variable, scenario_name=scenario,
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


@csrf_exempt
def populate_rrf_policy_datatables(request):
    body_unicode = request.body.decode('utf-8')

    if request.method == 'POST':
        q = RrfPolicy.objects.all()

        ls = []
        for item in q:
            temp = {
                "title": item.title,
                "description": item.description,
                "country": item.country,
                "budget": item.budget,
                "total_ratio": item.total_ratio,
                "first_classification": item.first_classification,
                "second_classification": item.second_classification
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


def rrf_landing(request):
    context = {}
    return render(request, 'i2amparis_main/rrf_policy_workspace/rrf_policy_intro.html', context)


def eu_workspace_landing(request):
    context = {}
    return render(request, 'i2amparis_main/eu_workspace/eu_workspace_landing.html', context)


def euw_harmonisation(request):
    models = ModelsInfo.objects.all().filter(
        model_name__in=['aladin', 'eu_times', 'e3me', 'forecast', 'gcam', 'gemini_e3', 'ices', 'muse', 'nemesis',
                        'tiam', '42']).order_by('model_title')
    variables = Harmonisation_Variables.objects.all().order_by('order')

    if not os.path.isfile('cached_data/harmonisation_heatmaps/pr_harmonisation_heatmap.json'):
        var_mod_data = EUHarmData.objects.filter(
            model__name__in=['aladin', 'eu_times', 'e3me', 'forecast', 'gcam', 'gemini_e3', 'ices', 'muse', 'nemesis',
                             'tiam', '42'])
        harm_data_sources_links = HarmDataSourcesLinks.objects.filter(
            model__name__in=['aladin', 'eu_times', 'e3me', 'forecast', 'gcam', 'gemini_e3', 'ices', 'muse', 'nemesis',
                             'tiam', '42'])
        var_mod = create_info_for_var_harmonisation_heatmaps(harm_data_sources_links, var_mod_data)
    else:
        print('Heatmap is cached! Loading file...')
        with open('cached_data/harmonisation_heatmaps/pr_harmonisation_heatmap.json') as f:
            data = f.read()
        var_mod = json.loads(data)
    context = {"models": models,
               "variables": variables,
               "var_mod": var_mod}
    return render(request, 'i2amparis_main/eu_workspace/euw_harmonisation.html', context)


def euw_scientific_module(request):
    models = DataVariablesModels.objects.filter(
        name__in=['aladin', 'eu_times', 'e3me', 'forecast', 'gcam', 'gemini_e3', 'ices', 'muse', 'nemesis', 'tiam',
                  '42']).order_by('title')
    scenarios = ScenariosRes.objects.filter(name__in=['EUWWH']).order_by('title')
    regions = RegionsRes.objects.filter(name='EU')
    filter_vars = PRWEUMetaData.objects.values('variable_name').distinct()
    var_list = [x['variable_name'] for x in filter_vars]
    variables = VariablesRes.objects.filter(name__in=var_list).order_by('ordering')
    units = UnitsRes.objects.all().order_by('title')

    context = {"models": models,
               "variables": variables,
               "scenarios": scenarios,
               "regions": regions,
               "units": units}

    return render(request, 'i2amparis_main/eu_workspace/euw_scientific_module.html', context)


def euw_public_ui(request):
    context = {}
    return render(request, 'i2amparis_main/eu_workspace/euw_public_ui.html', context)


def euw_virtual_library(request, **kwargs):
    if 'section' not in kwargs.keys():
        context = {}
        return render(request, 'i2amparis_main/eu_workspace/euw_virtual_library.html', context)
    else:
        context = {}
        return render(request, 'i2amparis_main/eu_workspace/euw_virtual_library_' + kwargs['section'] + '.html',
                      context)


def detailed_model_doc(request, model=''):
    if model == '':
        print('Detailed Model Documentation')
        sel_project = request.GET.get('project', 'All')
        list_of_models = ModelsInfo.objects.all().order_by('model_title')
        model_objs = []

        for model in list_of_models:
            projects = ProjectModels.objects.filter(model_id=model.id)
            temp_list = []
            model_dict = {}
            for project in projects:
                temp_list.append(project.project)
            model_dict['object'] = model
            model_dict['projects'] = temp_list
            model_objs.append(model_dict)

        sel_icons = 'rev_icons'
        context = {
            'model_list': model_objs,
            'sel_icons': sel_icons,
            'sel_project': sel_project
        }
        return render(request, 'i2amparis_main/detailed_documentation/detailed_model_documentation_landing_page.html',
                      context)
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

        return render(request, 'i2amparis_main/detailed_documentation/detailed_' + model + '.html',
                      context={'menu_models': model_dict, 'coverage': menu_cat})


def dynamic_doc(request, model=''):
    template_format = request.GET.get('format')
    db = countries_data.RetriveDB(model)
    data = db.create_json()
    list_of_models = db.create_models_btn()
    for model_name in list_of_models:
        projects = ProjectModels.objects.filter(model__model_name=model_name)
        temp_list = []
        for project in projects:
            temp_list.append(project.project)
        list_of_models[model_name]['projects'] = temp_list

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
        template = 'i2amparis_main/dynamic_documentation/dynamic_documentation_final' + template_format + '.html'
    else:
        template = 'i2amparis_main/dynamic_documentation/dynamic_documentation_final.html'
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
