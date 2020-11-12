from django.urls import path, include

from . import views

urlpatterns = [
    path('main', views.landing_page, name='landing_page'),
    path('overview_comparative_assessment_doc', views.overview_comparative_assessment_doc, name='overview_comparative_assessment_doc'),
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
    path('getselectview', views.getselectview, name='getselectview')
]
