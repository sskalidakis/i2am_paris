from django.urls import path

from . import views

urlpatterns = [
    path('main', views.landing_page, name='landing_page'),
    path('overview_comparative_assessment_doc', views.overview_comparative_assessment_doc, name='overview_comparative_assessment_doc'),
]