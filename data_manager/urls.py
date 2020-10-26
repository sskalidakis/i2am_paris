from django.urls import path, include

from . import views

urlpatterns = [
    path('create_query', views.create_query, name='create_query'),
    path('delete_query', views.delete_query, name='delete_query'),
    path('test', views.datamanager_template, name='datamanager_template'),
]