from django.urls import path

from . import views


urlpatterns = [
    path('show_line_chart', views.show_line_chart, name='show_line_chart'),
    path('show_column_chart', views.show_column_chart, name='show_column_chart'),
    path('sankey_diagram', views.sankey_diagram, name='sankey_diagram'),
    path('chord_diagram', views.chord_diagram, name='chord_diagram'),
    path('heat_map', views.heat_map, name='heat_map'),
    path('bar_heat_map', views.bar_heat_map, name='bar_heat_map'),
    path('horizontal_dumbbell', views.horizontal_dumbbell, name='horizontal_dumbbell'),
]