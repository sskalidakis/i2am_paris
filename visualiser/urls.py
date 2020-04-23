from django.urls import path

from . import views


urlpatterns = [
    path('show_line_chart', views.show_line_chart, name='show_line_chart'),
    path('show_column_chart', views.show_column_chart, name='show_column_chart'),
    path('show_range_chart', views.show_range_chart, name='show_range_chart'),
    path('show_bar_range_chart', views.show_bar_range_chart, name='show_bar_range_chart'),
    path('show_stacked_column_chart', views.show_stacked_column_chart, name='show_stacked_column_chart'),
    path('show_bar_heat_map_chart', views.bar_heat_map, name='show_bar_heat_map_chart'),
    path('sankey_diagram', views.sankey_diagram, name='sankey_diagram'),
    path('chord_diagram', views.chord_diagram, name='chord_diagram'),
    path('show_heat_map', views.heat_map_on_map, name='heat_map'),
]