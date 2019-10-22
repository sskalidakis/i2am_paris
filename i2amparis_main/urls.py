from django.urls import path

from . import views

urlpatterns = [
    path('main', views.landing_page, name='landing_page'),
    path('overview_comparative_assessment_doc', views.overview_comparative_assessment_doc, name='overview_comparative_assessment_doc'),
    path('dynamic_doc', views.dynamic_doc, name='dynamic_doc'),
    path('dynamic_doc/<str:model>', views.dynamic_doc, name='dynamic_doc_model')
    # path('<str:model>', views.dynamic_doc, name='dynamic_doc'),
]