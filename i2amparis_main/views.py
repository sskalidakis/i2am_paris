from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import countries_data
from django.utils.html import format_html
from i2amparis_main.models import ModelsInfo, Harmonisation_Variables, HarmDataNew, HarmDataSourcesLinks, ScenariosRes, \
    RegionsRes, ResultsComp, VariablesRes, UnitsRes, DataVariablesModels, HarmDataSourcesTitles
from django.core.mail import send_mail
from .forms import FeedbackForm
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.db.models import Count

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
    models = DataVariablesModels.objects.all().order_by('title')
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
def update_scientific_model_selects(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if request.method == 'POST':
        models = body['model__name']
        scenarios = body['scenario__name']
        regions = body['region__name']
        variables = body['variable__name']
        changed = body['changed']

        all_models = [el.name for el in DataVariablesModels.objects.all()]
        all_scenarios = [el.name for el in ScenariosRes.objects.all()]
        all_regions = [el.name for el in RegionsRes.objects.all()]
        all_variables = [el.name for el in VariablesRes.objects.all()]

        if len(models) == 0:
            models = all_models

        if len(scenarios) == 0:
            scenarios = all_scenarios

        if len(regions) == 0:
            regions = all_regions

        if len(variables) == 0:
            variables = all_variables

        distinct_choices = ResultsComp.objects.filter(model__name__in=models, scenario__name__in=scenarios,
                                                      region__name__in=regions,
                                                      variable__name__in=variables).values('model__name',
                                                                                           'scenario__name',
                                                                                           'region__name',
                                                                                           'variable__name').distinct()
        allowed_models = []
        allowed_scenarios = []
        allowed_variables = []
        allowed_regions = []

        for choice in distinct_choices:
            if choice['model__name'] not in allowed_models:
                allowed_models.append(choice['model__name'])
            if choice['scenario__name'] not in allowed_scenarios:
                allowed_scenarios.append(choice['scenario__name'])
            if choice['region__name'] not in allowed_regions:
                allowed_regions.append(choice['region__name'])
            if choice['variable__name'] not in allowed_variables:
                allowed_variables.append(choice['variable__name'])

        
        ls = {'models': [el for el in all_models if el not in allowed_models],
              'scenarios': [el for el in all_scenarios if el not in allowed_scenarios],
              'regions': [el for el in all_regions if el not in allowed_regions],
              'variables': [el for el in all_variables if el not in allowed_variables]}

        return JsonResponse(ls, safe=False)


@csrf_exempt
def populate_scientific_module_datatables(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if request.method == 'POST':
        print("----------------------------------")
        models = body['model__name']
        scenarios = body['scenario__name']
        regions = body['region__name']
        variables = body['variable__name']

        print("models = ", models)
        print("scenarios = ", scenarios)
        print("regions = ", regions)
        print("variables = ", variables)

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
