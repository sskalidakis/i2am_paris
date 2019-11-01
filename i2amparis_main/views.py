from django.shortcuts import render
from . import countries_data
from django.utils.html import format_html
from i2amparis_main.models import ModelsInfo

def landing_page(request):
    print ('Landing page')
    return render(request, 'i2amparis_main/landing_page.html')

def overview_comparative_assessment_doc(request):
    print('Overview Comparative Assessment')
    return render(request, 'i2amparis_main/overview_comparative_assessment_doc.html')

def dynamic_doc(request, model=''):

    template_format = request.GET.get('format')
    db = countries_data.RetriveDB(model)
    data = db.create_json()
    list_of_models = db.create_models_btn()
    # import pdb
    # pdb.set_trace()
    context = {
        'data': data,
        'buttons': list_of_models,
        'granularities': db.retrieve_granularity,
        'selected_model': ModelsInfo.objects.get(id=db.model_id).model_name,
        'template_format': template_format
    }
    if template_format is not None:
        template = 'i2amparis_main/dynamic_documentation_final' + template_format + '.html'
    else:
        template = 'i2amparis_main/dynamic_documentation_final.html'
    return render(request, template, context)
