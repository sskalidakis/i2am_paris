from django.apps import apps

from i2amparis_main.models import DataVariablesModels, ScenariosRes, RegionsRes, VariablesRes, PRWEUMetaData, \
    PRWMetaData


def get_model_by_db_table(db_table):
    for model in apps.get_models():
        if model._meta.db_table == db_table:
            return model
    else:
        # here you can do fallback logic if no model with db_table found
        raise ValueError('No model found with db_table {}!'.format(db_table))
        # or return None


def get_initial_detailed_conf_analysis_form_data(interface):
    if interface == 'pr_global':
        all_models = [el['name'] for el in DataVariablesModels.objects.filter(
            name__in=['42', 'e3me', 'gcam', 'gemini_e3', 'ices', 'muse', 'tiam']).values('name')]
        all_scenarios = [el['name'] for el in ScenariosRes.objects.exclude(name='EUWWH').values('name')]
        all_regions = [el['name'] for el in RegionsRes.objects.values('name')]
        all_variables = [el['variable_name'] for el in PRWMetaData.objects.distinct().values('variable_name')]
        metadata = PRWMetaData
        return all_models, all_scenarios, all_regions, all_variables, metadata
    elif interface == 'pr_eu':
        all_models = [el['name'] for el in DataVariablesModels.objects.filter(
            name__in=['aladin', 'eu_times', 'e3me', 'forecast', 'gcam', 'gemini_e3', 'ices', 'muse', 'nemesis', 'tiam', '42']).values('name')]
        all_scenarios = [el['name'] for el in ScenariosRes.objects.filter(name='EUWWH').values('name')]
        all_regions = [el['name'] for el in RegionsRes.objects.filter(name='EU').values('name')]
        all_variables = [el['variable_name'] for el in PRWEUMetaData.objects.distinct().values('variable_name')]
        metadata = PRWEUMetaData
        return all_models, all_scenarios, all_regions, all_variables, metadata
    else:
        print('No interface provided or no interface exists with that name!')