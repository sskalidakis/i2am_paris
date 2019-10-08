from django.urls import path

from . import views

urlpatterns = [
    path('main', views.landing_page, name='landing_page'),
]