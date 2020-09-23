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
    path('paris_reinforce_workspace', views.paris_reinforce_workspace, name='paris_reinforce_workspace'),
    # path('', include('visualiser.urls')),
    # path('', include('feedback_form.urls')),
    # path('<str:model>', views.dynamic_doc, name='dynamic_doc'),
]