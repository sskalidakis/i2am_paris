from django.shortcuts import render
from . import countries_data
from django.utils.html import format_html


def landing_page(request):
    print ('Landing page')
    return render(request, 'i2amparis_main/landing_page.html')

def overview_comparative_assessment_doc(request):
    print('Overview Comparative Assessment')
    return render(request, 'i2amparis_main/overview_comparative_assessment_doc.html')

def dynamic_doc(request, model=''):
    db = countries_data.RetriveDB(model)
    data = db.create_json()

    print(db.retrieve_mitigation_adaption())
    print(db.retrieve_policy())

    list_of_models = db.create_models_btn()
    context = {
        'data': data,
        'sectors': format_html(db.retrive_granularity("sectoral")),
        'emission': format_html(db.retrive_granularity("emission")),
        'socioecon': format_html(db.retrive_granularity("socioecon")),
        'buttons': list_of_models,
        'test': db.retrieve_mitigation_adaption()
    }
    return render(request, 'i2amparis_main/dynamic_documentation.html', context)
