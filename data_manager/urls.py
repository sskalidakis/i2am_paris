from django.urls import path, include

from . import views

urlpatterns = [
    path('create_query', views.create_query, name='create_query'),
    path('delete_query', views.delete_query, name='delete_query'),
    path('retrieve_series_info', views.retrieve_series_info, name="retrieve_series_info"),
    path('retrieve_series_info_fossil_energy_co2', views.retrieve_series_info_fossil_energy_co2, name="retrieve_series_info_fossil_energy_co2"),
    path('receive', views.receive_data, name='receive_data'),
]