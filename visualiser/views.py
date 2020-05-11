from json import JSONDecodeError

from django.shortcuts import render

from django.http import HttpResponse

from visualiser.fake_data.fake_data import FAKE_DATA, COLUMNCHART_DATA, BAR_RANGE_CHART_DATA, BAR_HEATMAP_DATA, \
    HEAT_MAP_DATA, SANKEYCHORD_DATA, THERMOMETER, HEAT_MAP_CHART_DATA, PARALLEL_COORDINATES_DATA, PIE_CHART_DATA, \
    RADAR_CHART_DATA, PARALLEL_COORDINATES_DATA_2

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

from visualiser.utils import *
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
import json

class XYZ_chart:
    def __init__(self, request, x_axis_name, x_axis_title, x_axis_unit, y_axis_name, y_axis_title, y_axis_unit,
                 z_axis_name, z_axis_title, z_axis_unit, chart_data, color_list, minmax_z_value, chart_type):
        self.x_axis_name = x_axis_name
        self.x_axis_title = x_axis_title
        self.x_axis_unit = x_axis_unit
        self.y_axis_name = y_axis_name
        self.y_axis_title = y_axis_title
        self.y_axis_unit = y_axis_unit
        self.z_axis_name = z_axis_name
        self.z_axis_title = z_axis_title
        self.z_axis_unit = z_axis_unit
        self.chart_data = chart_data
        self.request = request
        self.chart_type = chart_type
        self.color_list = color_list
        self.minmax_z_value = minmax_z_value
        self.content = {'x_axis_title': self.x_axis_title, 'x_axis_unit': self.x_axis_unit,
                        'x_axis_name': self.x_axis_name, 'y_axis_title': self.y_axis_title,
                        'y_axis_unit': self.y_axis_unit, 'y_axis_name': self.y_axis_name,'z_axis_name': z_axis_name,
                        'z_axis_title': z_axis_title, 'z_axis_unit': z_axis_unit, 'color_list': self.color_list,
                        'minmax_z_value': self.minmax_z_value, 'chart_data': self.chart_data}

    def show_chart(self):
        if self.chart_type == 'heat_map_chart':
            return render(self.request, 'visualiser/heat_map_chart.html',
                          self.content)


class XY_chart:
    def __init__(self, request, x_axis_name, x_axis_title, x_axis_unit, y_var_names, y_var_titles, y_var_units,
                 x_axis_type, y_axis_title, chart_data, color_list, use_default_colors, chart_3d, minmax_y_value,
                 chart_type):
        self.x_axis_name = x_axis_name
        self.x_axis_title = x_axis_title
        self.x_axis_unit = x_axis_unit
        self.y_var_names = y_var_names
        self.y_var_titles = y_var_titles
        self.y_var_units = y_var_units
        self.x_var_type = x_axis_type
        self.chart_data = chart_data
        self.request = request
        self.chart_type = chart_type
        self.x_axis_type = x_axis_type
        self.y_axis_title = y_axis_title
        self.color_list = color_list
        self.use_default_colors = use_default_colors
        self.chart_3d = chart_3d
        self.minmax_y_value = minmax_y_value
        print(minmax_y_value)
        self.content = {'x_axis_title': self.x_axis_title, 'x_axis_unit': self.x_axis_unit,
                        'x_axis_name': self.x_axis_name, 'y_var_titles': self.y_var_titles,
                        'y_var_units': self.y_var_units, 'y_var_names': self.y_var_names,
                        'x_axis_type': self.x_axis_type, 'y_axis_title': self.y_axis_title,
                        'color_list': self.color_list, 'use_default_colors': self.use_default_colors,
                        'chart_3d': self.chart_3d, 'minmax_y_value': self.minmax_y_value, 'chart_data': self.chart_data}

    def show_chart(self):
        if self.chart_type == 'line_chart':
            return render(self.request, 'visualiser/line_chart_am4.html',
                          self.content)
        elif self.chart_type == 'column_chart':
            return render(self.request, 'visualiser/column_chart_am4.html',
                          self.content)
        elif self.chart_type == 'range_chart':
            return render(self.request, 'visualiser/range_chart_am4.html',
                          self.content)
        elif self.chart_type == 'bar_range_chart':
            return render(self.request, 'visualiser/bar_range_chart_am4.html',
                          self.content)
        elif self.chart_type == 'stacked_column_chart':
            return render(self.request, 'visualiser/stacked_column_chart_am4.html',
                          self.content)
        elif self.chart_type == 'bar_heat_map_chart':
            return render(self.request, 'visualiser/bar_heat_map.html',
                          self.content)
        elif self.chart_type == 'pie_chart':
            return render(self.request, 'visualiser/pie_chart.html',
                          self.content)
        elif self.chart_type == 'radar_chart':
            return render(self.request, 'visualiser/radar_chart.html',
                          self.content)

class FlowChart:
    """
    Sankey chart and Chord diagram have the same format of data

    """
    def __init__(self, request, data, node_list, pass_value, color_node_list, use_def_colors, chart_title, chart_type):
        """

        :param chart_type:
        :param data:
        """
        self.request = request
        self.chart_type = chart_type
        self.pass_value = pass_value
        self.node_list = node_list
        self.color_node_list = color_node_list
        self.use_def_colors = use_def_colors
        self.chart_title = chart_title
        self.data = data
        self.content = {"data": self.data, "pass_value": self.pass_value, "node_list": self.node_list,
                        "color_node_list": self.color_node_list, "use_default_colors": self.use_def_colors,
                        "chart_title": self.chart_title}

    def show_chart(self):
        """
        :return:
        """
        if (self.chart_type == "chord_diagram"):
            return render(self.request, 'visualiser/chord_diagram.html', self.content)
        elif (self.chart_type == "sankey_diagram"):
            return render(self.request, 'visualiser/sankey_diagram.html', self.content)

@csrf_exempt
def get_response_data_XY(request):
    if request.method == "GET":
        json_response = {
            "y_var_names": request.GET.getlist("y_var_names[]", []),
            "y_var_titles": request.GET.getlist("y_var_titles[]", []),
            "y_var_units": request.GET.getlist("y_var_units[]", []),
            "x_axis_type": request.GET.get("x_axis_type", ""),
            "x_axis_name": request.GET.get("x_axis_name", ""),
            "x_axis_title": request.GET.get("x_axis_title", ""),
            "x_axis_unit": request.GET.get("x_axis_unit", ""),
            "y_axis_title": request.GET.get("y_axis_title", ""),
            "color_list_request": request.GET.getlist("color_list_request[]", []),
            "use_default_colors": request.GET.get("use_default_colors", "true"),
            "chart_3d": request.GET.get("chart_3d", ""),
            "min_max_y_value": request.GET.getlist("min_max_y_value[]", []),
            "dataset": request.GET.get("dataset", ""),

        }
    else:
        json_response = json.loads(request.body)
        print(json_response)
    return json_response


@csrf_exempt
def show_line_chart(request):
    response_data = get_response_data_XY(request)
    print(response_data)
    y_var_names = response_data['y_var_names']
    y_var_titles = response_data['y_var_titles']
    y_var_units = response_data['y_var_units']
    x_axis_type = response_data['x_axis_type']
    x_axis_name = response_data['x_axis_name']
    x_axis_title = response_data['x_axis_title']
    x_axis_unit = response_data['x_axis_unit']
    y_axis_title = response_data['y_axis_title']
    color_list_request = response_data['color_list_request']
    use_default_colors = response_data['use_default_colors']
    chart_3d = ""
    min_max_y_value = response_data['min_max_y_value']
    dataset = response_data['dataset']

    # TODO: Create a method for getting the actual data from DBs, CSV files, dataframes??
    data = FAKE_DATA

    color_list = define_color_code_list(color_list_request)

    line_chart = XY_chart(request, x_axis_name, x_axis_title, x_axis_unit, y_var_names, y_var_titles, y_var_units,
                          x_axis_type, y_axis_title, data, color_list, use_default_colors, chart_3d, min_max_y_value,
                          'line_chart')
    return line_chart.show_chart()


@csrf_exempt
def show_column_chart(request):
    # Use get_response_data_XY to get the same variables
    response_data = get_response_data_XY(request)
    y_var_names = response_data["y_var_names"]
    y_var_titles = response_data["y_var_titles"]
    y_var_units = response_data["y_var_units"]
    x_axis_type = response_data["x_axis_type"]
    x_axis_name = response_data["x_axis_name"]
    x_axis_title = response_data["x_axis_title"]
    x_axis_unit = response_data["x_axis_unit"]
    y_axis_title = response_data["y_axis_title"]
    min_max_y_value = response_data["min_max_y_value"]
    color_list_request = response_data["color_list_request"]
    use_default_colors = response_data["use_default_colors"]
    chart_3d = response_data["chart_3d"]
    # TODO: Create a method for getting the actual data from DBs, CSV files, dataframes??
    # data = response_data["dataset"]
    data = COLUMNCHART_DATA
    # y_var_names = ["year2017", "year2018"]
    # y_var_titles = ["Year 2017", "Year 2018"]
    # y_var_units = ["%", "%"]
    # x_axis_type = "text"
    # x_axis_name = "country"
    # x_axis_title = "Country"
    # x_axis_unit = ""
    # y_axis_title = "GDP Rates"
    # color_list_request = ['blue', 'red', 'green']
    # use_default_colors = "false"
    # chart_3d = "true"
    # min_max_y_value = [0, 2000]
    # from pprint import pprint as pp
    # pp(response_data)
    # pp(response_data_col)
    color_list = define_color_code_list(color_list_request)
    column_chart = XY_chart(request, x_axis_name, x_axis_title, x_axis_unit, y_var_names, y_var_titles, y_var_units,
                            x_axis_type, y_axis_title, data, color_list, use_default_colors, chart_3d, min_max_y_value,
                            'column_chart')
    return column_chart.show_chart()


@csrf_exempt
def get_response_data_pie(request):
    if request.method == "GET":
        json_response = {
            "variable_name": request.GET.getlist("variable_name[]", []),
            "variable_title": request.GET.getlist("variable_title[]", []),
            "variable_unit": request.GET.getlist("variable_unit[]", []),
            "category_name": request.GET.get("category_name", ""),
            "category_title": request.GET.get("category_title", ""),
            "category_unit": request.GET.get("category_unit", "")
        }
    else:
        json_response = json.loads(request.body)
        print(json_response)
    return json_response


@csrf_exempt
def show_pie_chart(request):
    response_data_pie = get_response_data_pie(request)
    variable_name = response_data_pie["variable_name"]
    variable_title = response_data_pie["variable_title"]
    variable_unit = response_data_pie["variable_unit"]
    category_name = response_data_pie["category_name"]
    category_title = response_data_pie["category_title"]
    category_unit = response_data_pie["category_unit"]
    response_data_xy = get_response_data_XY(request)
    x_axis_type = response_data_xy["x_axis_type"]
    y_axis_title = response_data_xy["y_axis_title"]
    color_list_request = response_data_xy["color_list_request"]
    min_max_y_value = response_data_xy["min_max_y_value"]
    chart_3d = response_data_xy["chart_3d"]
    use_default_colors = response_data_xy["use_default_colors"]
    data = PIE_CHART_DATA
    # print(data)
    # variable_name = ["oil_consumption"]
    # variable_title = ["Oil Consumption"]
    # variable_unit = ["litres"]
    # x_axis_type = ""
    # category_name = "country"
    # category_title = "Country"
    # category_unit = ""
    # y_axis_title = ""
    # color_list_request = ['blue', 'red', 'green', "gold", "ceramic", "fuchsia", "violet", "purple", "cyan"]
    # use_default_colors = "false"
    # chart_3d = "false"
    # min_max_y_value = []
    color_list = define_color_code_list(color_list_request)

    pie_chart = XY_chart(request, category_name, category_title, category_unit, variable_name, variable_title, variable_unit,
                          x_axis_type, y_axis_title, data, color_list, use_default_colors, chart_3d, min_max_y_value,
                          'pie_chart')
    return pie_chart.show_chart()


def show_radar_chart(request):
    response_data_pie = get_response_data_pie(request)
    variable_name = response_data_pie["variable_name"]
    variable_title = response_data_pie["variable_title"]
    variable_unit = response_data_pie["variable_unit"]
    category_name = response_data_pie["category_name"]
    category_title = response_data_pie["category_title"]
    category_unit = response_data_pie["category_unit"]
    response_data_xy = get_response_data_XY(request)
    x_axis_type = response_data_xy["x_axis_type"]
    y_axis_title = response_data_xy["y_axis_title"]
    color_list_request = response_data_xy["color_list_request"]
    min_max_y_value = response_data_xy["min_max_y_value"]
    chart_3d = response_data_xy["chart_3d"]
    use_default_colors = response_data_xy["use_default_colors"]
    data = RADAR_CHART_DATA
    # variable_name = ["oil_consumption", "energy_consumption"]
    # variable_title = ["Oil Consumption", "Energy Consumption"]
    # variable_unit = ["litres", "Watt"]
    # x_axis_type = ""
    # category_name = "country"
    # category_title = "Country"
    # category_unit = ""
    # y_axis_title = ""
    # color_list_request = ['red', "blue"]
    # use_default_colors = "false"
    # chart_3d = "false"
    # min_max_y_value = []
    color_list = define_color_code_list(color_list_request)

    radar_chart = XY_chart(request, category_name, category_title, category_unit, variable_name, variable_title,
                           variable_unit, x_axis_type, y_axis_title, data, color_list, use_default_colors, chart_3d,
                           min_max_y_value, 'radar_chart')
    return radar_chart.show_chart()

def show_range_chart(request):
    response_data_xy = get_response_data_XY(request)
    y_var_names = response_data_xy['y_var_names']
    y_var_titles = response_data_xy['y_var_titles']
    y_var_units = response_data_xy['y_var_units']
    x_axis_type = response_data_xy['x_axis_type']
    x_axis_name = response_data_xy['x_axis_name']
    x_axis_title = response_data_xy['x_axis_title']
    x_axis_unit = response_data_xy['x_axis_unit']
    y_axis_title = response_data_xy['y_axis_title']
    color_list_request = response_data_xy['color_list_request']
    use_default_colors = response_data_xy['use_default_colors']
    min_max_y_value = response_data_xy["min_max_y_value"]
    chart_3d = response_data_xy["chart_3d"]
    data = FAKE_DATA
    # y_var_names = ["myVar1", "myVar2"]
    # y_var_titles = ["Var1", "Var2"]
    # y_var_units = ["v1_unit", "v2_unit"]
    # x_axis_type = "time"
    # x_axis_name = "time"
    # x_axis_title = "Time"
    # x_axis_unit = ""
    # y_axis_title = "Var"
    # color_list_request = ['blue', 'red', 'green']
    # use_default_colors = "false"
    # chart_3d = "false"
    # min_max_y_value = [0, 2000]

    color_list = define_color_code_list(color_list_request)

    range_chart = XY_chart(request, x_axis_name, x_axis_title, x_axis_unit, y_var_names, y_var_titles, y_var_units,
                           x_axis_type, y_axis_title, data, color_list, use_default_colors, chart_3d, min_max_y_value,
                           'range_chart')
    return range_chart.show_chart()


def show_bar_range_chart(request):
    response_data_xy = get_response_data_XY(request)
    y_var_names = response_data_xy['y_var_names']
    y_var_titles = response_data_xy['y_var_titles']
    y_var_units = response_data_xy['y_var_units']
    x_axis_type = response_data_xy['x_axis_type']
    x_axis_name = response_data_xy['x_axis_name']
    x_axis_title = response_data_xy['x_axis_title']
    x_axis_unit = response_data_xy['x_axis_unit']
    y_axis_title = response_data_xy['y_axis_title']
    color_list_request = response_data_xy['color_list_request']
    use_default_colors = response_data_xy['use_default_colors']
    min_max_y_value = response_data_xy["min_max_y_value"]
    chart_3d = response_data_xy["chart_3d"]
    data = BAR_RANGE_CHART_DATA
    # y_var_names = ["name"]
    # y_var_titles = ["Var1", "Var2"]
    # y_var_units = ["-"]
    # x_axis_type = "time"
    # x_axis_name = "time"
    # x_axis_title = "Time"
    # x_axis_unit = ""
    # y_axis_title = "Name"
    # color_list_request = ['blue', 'red', 'green','gold','mustard','purple','violet','ceramic']
    # use_default_colors = "false"
    color_list = define_color_code_list(color_list_request)
    # chart_3d = "false"
    # min_max_y_value = [0, 2000]
    bar_range_chart = XY_chart(request, x_axis_name, x_axis_title, x_axis_unit, y_var_names, y_var_titles, y_var_units,
                               x_axis_type, y_axis_title, data, color_list, use_default_colors, chart_3d,
                               min_max_y_value, 'bar_range_chart')
    return bar_range_chart.show_chart()


def show_stacked_column_chart(request):
    response_data_xy = get_response_data_XY(request)
    y_var_names = response_data_xy['y_var_names']
    y_var_titles = response_data_xy['y_var_titles']
    y_var_units = response_data_xy['y_var_units']
    x_axis_type = response_data_xy['x_axis_type']
    x_axis_name = response_data_xy['x_axis_name']
    x_axis_title = response_data_xy['x_axis_title']
    x_axis_unit = response_data_xy['x_axis_unit']
    y_axis_title = response_data_xy['y_axis_title']
    color_list_request = response_data_xy['color_list_request']
    use_default_colors = response_data_xy['use_default_colors']
    min_max_y_value = response_data_xy["min_max_y_value"]
    chart_3d = response_data_xy["chart_3d"]
    data = COLUMNCHART_DATA
    print(data)
    # y_var_names = ["year2017", "year2018"]
    # y_var_titles = ["Year 2017", "Year 2018"]
    # y_var_units = ["%", "%"]
    # x_axis_type = "text"
    # x_axis_name = "country"
    # x_axis_title = "Country"
    # x_axis_unit = ""
    # y_axis_title = "GDP Rates"
    # color_list_request = ['blue', 'red', 'green']
    # use_default_colors = "false"
    # chart_3d = "true"
    # min_max_y_value = [0, 2000]
    color_list = define_color_code_list(color_list_request)
    stacked_column_chart = XY_chart(request, x_axis_name, x_axis_title, x_axis_unit, y_var_names, y_var_titles, y_var_units,
                            x_axis_type, y_axis_title, data, color_list, use_default_colors, chart_3d, min_max_y_value,
                                    'stacked_column_chart')

    return stacked_column_chart.show_chart()


def show_bar_heat_map(request):
    response_data_xy = get_response_data_XY(request)
    y_var_names = response_data_xy['y_var_names']
    y_var_titles = response_data_xy['y_var_titles']
    y_var_units = response_data_xy['y_var_units']
    x_axis_type = response_data_xy['x_axis_type']
    x_axis_name = response_data_xy['x_axis_name']
    x_axis_title = response_data_xy['x_axis_title']
    x_axis_unit = response_data_xy['x_axis_unit']
    y_axis_title = response_data_xy['y_axis_title']
    color_list_request = response_data_xy['color_list_request'][0]
    use_default_colors = response_data_xy['use_default_colors']
    min_max_y_value = response_data_xy["min_max_y_value"]
    chart_3d = response_data_xy["chart_3d"]
    data = BAR_HEATMAP_DATA
    print(data)
    # y_var_names = ["value"]
    # y_var_titles = ["Value"]
    # y_var_units = ["units"]
    # x_axis_type = "text"
    # x_axis_name = "category"
    # x_axis_title = "Category"
    # x_axis_unit = ""
    # y_axis_title = "Value Units"
    # color_list_request = "blue_red"
    # use_default_colors = "false"
    # chart_3d = "false"
    # min_max_y_value = [0, 2000]
    # TODO check this color_list_request
    color_couple = AM_CHARTS_COLOR_HEATMAP_COUPLES[color_list_request]
    bar_heat_map_chart = XY_chart(request, x_axis_name, x_axis_title, x_axis_unit, y_var_names, y_var_titles,
                                  y_var_units, x_axis_type, y_axis_title, data, color_couple, use_default_colors,
                                  chart_3d, min_max_y_value, 'bar_heat_map_chart')

    return bar_heat_map_chart.show_chart()


@csrf_exempt
def get_response_heat_map(request):
    if request.method == "GET":
        json_response = {
            "z_axis_name": request.GET.get("z_axis_name", ""),
            "z_axis_title": request.GET.get("z_axis_title", ""),
            "z_axis_unit": request.GET.get("z_axis_unit", ""),
            "min_max_z_value": request.GET.getlist("min_max_z_value[]", []),
        }
    else:
        json_response = json.loads(request.body)
        print(json_response)
    return json_response


def show_heat_map_chart(request):
    response_data_xy = get_response_data_XY(request)
    y_axis_name = response_data_xy['y_var_names'][0]
    y_axis_unit = response_data_xy['y_var_units'][0]
    x_axis_name = response_data_xy['x_axis_name']
    x_axis_title = response_data_xy['x_axis_title']
    x_axis_unit = response_data_xy['x_axis_unit']
    y_axis_title = response_data_xy['y_axis_title']
    color_list_request = response_data_xy['color_list_request'][0]
    response_heat_map = get_response_heat_map(request)
    z_axis_name = response_heat_map["z_axis_name"]
    z_axis_title = response_heat_map["z_axis_title"]
    z_axis_unit = response_heat_map["z_axis_unit"]
    min_max_z_value = response_heat_map["min_max_z_value"]
    data = HEAT_MAP_CHART_DATA
    # y_axis_name = 'hour'
    # y_axis_title = 'Hour'
    # y_axis_unit = '-'
    # x_axis_name = "weekday"
    # x_axis_title = "Weekday"
    # x_axis_unit = "-"
    # z_axis_name = "value"
    # z_axis_title = "Value"
    # z_axis_unit = "m"
    # color_list_request = "cyan"
    # min_max_z_value = [1900, 11000]
    color_list = AM_CHARTS_COLOR_HEATMAP_COUPLES.get(color_list_request, define_color_code_list([color_list_request]))
    bar_heat_map_chart = XYZ_chart(request, x_axis_name, x_axis_title, x_axis_unit, y_axis_name, y_axis_title,
                                   y_axis_unit, z_axis_name, z_axis_title, z_axis_unit, data, color_list,
                                   min_max_z_value, 'heat_map_chart')

    return bar_heat_map_chart.show_chart()


@csrf_exempt
def get_response_sankey_diagram(request):
    if request.method == "GET":
        json_response = {
            "pass_value": request.GET.get("pass_value", ""),
            "use_def_colors": request.GET.get("use_def_colors", "false"),
            "chart_title": request.GET.get("chart_title", ""),
            "node_list": request.GET.getlist("node_list[]", []),
            "color_node_list": request.GET.getlist("color_node_list[]", []),
        }
    else:
        json_response = json.loads(request.body)
        print(json_response)
    return json_response


def sankey_diagram(request):
    """
    As input we will take a dict with key the begin and value a list with first element end and second the value
    :param request:
    :return:
    """
    response_sankey_diagram = get_response_sankey_diagram(request)
    pass_value = response_sankey_diagram["pass_value"]
    node_list = response_sankey_diagram["node_list"]
    use_def_colors = response_sankey_diagram["use_def_colors"]
    chart_title = response_sankey_diagram["chart_title"]
    color_node_list = response_sankey_diagram["color_node_list"]
    # From utils use AM_CHARTS_COLOR_CODES_LIST to convert colors' names to hex code of given colors
    # TODO use get and define a default color in case the given color doesnt appear in AM_CHARTS_COLOR_CODES_LIST
    color_node_list = [AM_CHARTS_COLOR_CODES_LIST[color_name] for color_name in color_node_list]
    # pass_value = "meat"
    data = SANKEYCHORD_DATA
    # node_list = ["A", "B", "C", "D", "E", "G", "H", "I", "J"]
    # color_node_list = ["#93B5C6", "#DDEDAA", "#BD4F6C", "#D7816A", "#BEC5AD", "#13B5C6", "#DDEDfA","#A0CF65", "#BDFF6C"]
    # use_def_colors = "false"
    # chart_title = "Sankey Flow Chart of Business Processes"
    sankey_diagram = FlowChart(request, data, node_list, pass_value, color_node_list, use_def_colors, chart_title, 'sankey_diagram')
    return sankey_diagram.show_chart()


def chord_diagram(request):
    """
    As in put we will take a dict with key the begin and value a list with first element end and second the value
    :param request:
    :return:
    """
    response_sankey_diagram = get_response_sankey_diagram(request)
    pass_value = response_sankey_diagram["pass_value"]
    node_list = response_sankey_diagram["node_list"]
    use_def_colors = response_sankey_diagram["use_def_colors"]
    chart_title = response_sankey_diagram["chart_title"]
    color_node_list = response_sankey_diagram["color_node_list"]
    # From utils use AM_CHARTS_COLOR_CODES_LIST to convert colors' names to hex code of given colors
    # TODO use get and define a default color in case the given color doesnt appear in AM_CHARTS_COLOR_CODES_LIST
    color_node_list = [AM_CHARTS_COLOR_CODES_LIST[color_name] for color_name in color_node_list]
    # pass_value = "value"
    data = SANKEYCHORD_DATA
    # node_list = ["A", "B", "C", "D", "E", "G", "H", "I", "J"]
    # color_node_list = ["#93B5C6", "#DDEDAA", "#BD4F6C", "#D7816A", "#BEC5AD", "#13B5C6", "#DDEDfA","#A0CF65", "#BDFF6C"]
    # use_def_colors = "true"
    # chart_title = "Chord Flow Chart of Business Processes"
    chord_diagram = FlowChart(request, data, node_list, pass_value, color_node_list, use_def_colors, chart_title, 'chord_diagram')
    return chord_diagram.show_chart()


@csrf_exempt
def get_response_parallel_coordinates_chart(request):
    # TODO slice_size and samples_size are the same thing
    if request.method == "GET":
        json_response = {
            "y_axes": request.GET.getlist("y_axes[]", []),
            "title": request.GET.get("title", ""),
            "about_title": request.GET.get("title", ""),
            "about_text": request.GET.get("text", ""),
            "groups_title": request.GET.get("groups_title", ""),
            "samples_size": request.GET.get("samples_size", "10"),

        }
    else:
        json_response = json.loads(request.body)
        print(json_response)
    return json_response


def parallel_coordinates_chart(request):
    """
    y_axes the name of columns
    data a list of lists, each list must have the same length of y_axes
    slice_size define how much rows be visualid, in table below graph

    :param request:
    :return:
    """
    response_parallel_coordinates_chart = get_response_parallel_coordinates_chart(request)
    y_axes = response_parallel_coordinates_chart["y_axes"]
    slice_size = response_parallel_coordinates_chart["samples_size"]
    data = PARALLEL_COORDINATES_DATA
    # y_axes = ["A", "B", "C", "D", "E", "F"]
    # slice_size = 4
    return render(request, 'visualiser/parallel_coordinates_chart.html', {"y_axes": y_axes, "data": data, "slice_size": slice_size})


@csrf_exempt
def get_response_heat_map_on_map(request):
    if request.method == "GET":
        json_response = {
            "projection": request.GET.get("projection", ""),
            "map_var_name": request.GET.get("map_var_name", ""),
            "map_var_title": request.GET.get("map_var_title", ""),
            "map_var_unit": request.GET.get("map_var_unit", "")
        }
    else:
        json_response = json.loads(request.body)
        print(json_response)
    return json_response


def heat_map_on_map(request):
    response_heat_map_on_map = get_response_heat_map_on_map(request)
    projection = response_heat_map_on_map["projection"]
    map_var_name = response_heat_map_on_map["map_var_name"]
    map_var_title = response_heat_map_on_map["map_var_title"]
    map_var_unit = response_heat_map_on_map["map_var_unit"]
    response_data_xy = get_response_data_XY(request)
    color_list_request = response_data_xy["color_list_request"][0]
    min_max_y_value = response_data_xy["min_max_y_value"]
    map_data = HEAT_MAP_DATA
    # projection = ""
    # color_list_request = "blue_red"
    # min_max_y_value = [18, 45]
    # map_var_name = "temperature"
    # map_var_title = "Temperature"
    # map_var_unit = "C degrees"
    # projection = "eckert6"
    color_couple = AM_CHARTS_COLOR_HEATMAP_COUPLES[color_list_request]
    return render(request, 'visualiser/heat_map_on_map.html',
                  {"map_data": map_data, "projection": projection, "color_list": color_couple,
                   "map_var_name": map_var_name, "map_var_title": map_var_title, "map_var_unit": map_var_unit,
                   "minmax_y_value": min_max_y_value})


def thermometer_chart(request):
    recordData = {}
    for i in range(1, 11):
        temp = []
        for j in THERMOMETER:
            t = {"date": j["date"], "value": j["value"] * i}
            temp.append(t)
        recordData[i] = temp
    # min_max_y_value
    response_thermometer_chart = get_response_data_XY(request)
    min_max_temp = response_thermometer_chart["min_max_y_value"]
    # response_thermometer_chart =get_response_thermometer_chart(request)
    # min_max_temp = response_thermometer_chart["min_max_temp"]
    min_temp = min_max_temp[0]
    max_temp = min_max_temp[1]
    # min_temp = -20
    # max_temp = 50
    return render(request, 'visualiser/thermometer_chart.html', {"data": THERMOMETER, "recordData": recordData,
                                                                 "min_temp": min_temp, "max_temp": max_temp})


def parallel_coordinates_chart2(request):
    """

    :param request:
    :return:
    """
    # response_parallel_coordinates_chart2 = get_response_parallel_coordinates_chart2(request)
    response_parallel_coordinates_chart2 = get_response_parallel_coordinates_chart(request)
    y_axes = response_parallel_coordinates_chart2["y_axes"]
    title = response_parallel_coordinates_chart2["title"]
    about_title = response_parallel_coordinates_chart2["about_title"]
    about_text = response_parallel_coordinates_chart2["about_text"]
    groups_title = response_parallel_coordinates_chart2["groups_title"]
    sample_size = response_parallel_coordinates_chart2["samples_size"]
    # y_axes = [
    #             'name',
    #             'group',
    #             'protein (g)',
    #             'calcium (g)',
    #             'sodium (g)',
    #             'fiber (g)',
    #             'vitaminc (g)',
    #             'potassium (g)',
    #             'carbohydrate (g)',
    #             'sugars (g)',
    #             'fat (g)',
    #             'water (g)',
    #             'calories',
    #             'saturated (g)',
    #             'monounsat (g)',
    #             'polyunsat (g)'
    # ]
    data = PARALLEL_COORDINATES_DATA_2
    # title = "Nutrient Explorer"
    # about_title = "About"
    # about_text = "Write about this chart something"
    # groups_title = "Groups"
    # sample_size = 20
    samples_title = "Sample of %s entries" %sample_size
    # Create the variable colored_groups
    # First get the unique groups of give data
    groups_list = list(set(map(lambda x: x[1], data)))
    colored_groups = {}
    for k, group in enumerate(groups_list):
        colored_groups[group] = D3_PARALLEL_COORDINATES_COLORS[k]
    # Greate a dict with keys the name of groups and value a list which represent the HSL color
    # TODO get and set the colors in utils.py and pick for each given group
    # colored_groups = {
    #                           "Baby Foods": [185,56,73],
    #                           "Baked Products": [37,50,75],
    #                           "Beef Products": [325,50,39],
    #                           "Beverages": [10,28,67],
    #                           "Breakfast Cereals": [271,39,57],
    #                           "Cereal Grains and Pasta": [56,58,73],
    #                           "Dairy and Egg Products": [28,100,52],
    #                           "Ethnic Foods": [41,75,61],
    #                           "Fast Foods": [60,86,61],
    #                           "Fats and Oils": [30,100,73],
    #                           "Finfish and Shellfish Products": [318,65,67],
    #                           "Fruits and Fruit Juices": [274,30,76],
    #                           "Lamb, Veal, and Game Products": [20,49,49],
    #                           "Legumes and Legume Products": [334,80,84],
    #                           "Meals, Entrees, and Sidedishes": [185,80,45],
    #                           "Nut and Seed Products": [10,30,42],
    #                           "Pork Products": [339,60,49],
    #                           "Poultry Products": [359,69,49],
    #                           "Restaurant Foods": [204,70,41],
    #                           "Sausages and Luncheon Meats": [1,100,79],
    #                           "Snacks": [189,57,75],
    #                           "Soups, Sauces, and Gravies": [110,57,70],
    #                           "Spices and Herbs": [214,55,79],
    #                           "Sweets": [339,60,75],
    #                           "Vegetables and Vegetable Products": [120,56,40]
    #                             }
    return render(request, 'visualiser/parallel_coordinates_chart2.html', {
                                                                            "data": data,
                                                                            "y_axes": y_axes,
                                                                            "title": title,
                                                                            "about": about_title,
                                                                            "about_text": about_text,
                                                                            "groups": groups_title,
                                                                            "samples": samples_title,
                                                                            "samples_size": sample_size,
                                                                            "colored_groups": colored_groups
    })

