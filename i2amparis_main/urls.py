from django.urls import path, include

from . import views

urlpatterns = [
    path('main', views.landing_page, name='landing_page'),
    path('overview_comparative_assessment_doc', views.overview_comparative_assessment_doc,
         name='overview_comparative_assessment_doc'),
    path('overview_comparative_assessment_doc/global', views.overview_comparative_assessment_doc_global,
         name='overview_comparative_assessment_doc_global'),
    path('overview_comparative_assessment_doc/national_eu', views.overview_comparative_assessment_doc_national_eu,
         name='overview_comparative_assessment_doc_national_eu'),
    path('overview_comparative_assessment_doc/national_oeu', views.overview_comparative_assessment_doc_national_oeu,
         name='overview_comparative_assessment_doc_national_oeu'),
    path('detailed_model_doc', views.detailed_model_doc,
         name='detailed_model_doc'),
    path('detailed_model_doc/<model>', views.detailed_model_doc,
         name='detailed_model_doc_sel_model'),
    path('dynamic_doc/', views.dynamic_doc, name='dynamic_doc'),
    path('dynamic_doc/<str:model>/', views.dynamic_doc, name='dynamic_doc_model'),
    path('contact_form', views.contact_form, name='contact_form'),
    path('pr_wwh_landing', views.paris_reinforce_landing, name='paris_workspace_landing'),
    path('pr_wwh/harmonisation_table', views.paris_reinforce_harmonisation, name='paris_reinforce_harmonisation'),
    path('pr_wwh/scientific_module', views.paris_advanced_scientific_module, name='paris_advanced_scientific_module'),
    path('populate_detailed_analysis_datatables', views.populate_detailed_analysis_datatables,
         name='populate_detailed_analysis_datatables'),
    path('pr_wwh/conclusions', views.paris_cwdtm, name='paris_cool_what_does_this_mean'),

    path('update_scientific_model_selects_strict', views.update_scientific_model_selects_strict,
         name='update_scientific_model_selects_strict'),
    path('update_scientific_model_selects_basic', views.update_scientific_model_selects_basic,
         name='update_scientific_model_selects_basic'),
    path('get_sdg_variables', views.get_sdg_variables, name='get_sdg_variables'),
    path('rrf_policy_intro', views.rrf_landing, name='rrf_landing'),
    path('populate_rrf_policy_datatables', views.populate_rrf_policy_datatables,
         name='populate_rrf_policy_datatables'),
    path('euw_public_ui', views.euw_public_ui, name='euw_public_ui'),
    path('euw_virtual_library', views.euw_virtual_library, name='euw_virtual_library'),
    # path('update_comparative_selects_strict', views.update_comparative_selects_strict,
    #      name='update_comparative_selects_strict'),
    # path('update_comparative_selects_basic', views.update_comparative_selects_basic,
    #      name='update_comparative_selects_basic')
]
