from django.shortcuts import render

from django.http import HttpResponse

from visualiser.fake_data.fake_data import FAKE_DATA, COLUMNCHART_DATA, BAR_RANGE_CHART_DATA, BAR_HEATMAP_DATA

AM_CHARTS_COLOR_INDEX_LIST = {
    "light_blue": 0,
    "blue": 1,
    "violet_blue": 2,
    "purple": 4,
    "fuchsia": 7,
    "red": 8,
    "ceramic": 9,
    "light_brown": 10,
    "mustard": 11,
    "light_green": 13,
    "green": 16,
    "cyan": 19,
}

AM_CHARTS_COLOR_HEATMAP_COUPLES = {
    "blue_red": ["#539ad6", "#aa352f"],
    "green_red": ["#74b377", "#bf333c"],
    "brown_purple": ["#eeba95", "#74397a"],
    "purple_orange": ["#e6c8ee", "#db7c3d"],
    "cyan_green": ["#89c3c2", "#4b6822"],
    "yellow_gold": ["#f7ecc2", "#f5b500"],
    "beige_red": ["#f7dfd0", "#8d1915"],
    "grey_darkblue": ["#eaecf7", "#1f3b5e"],
    "lightblue_green": ["#bbe1ff", "#2e5c20"]

}


class XY_chart:
    def __init__(self, request, x_axis_name, x_axis_title, x_axis_unit, y_var_names, y_var_titles, y_var_units,
                 x_axis_type, y_axis_title, chart_data, color_list, use_default_colors, chart_3d, chart_type):
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
        self.content = {'x_axis_title': self.x_axis_title, 'x_axis_unit': self.x_axis_unit,
                        'x_axis_name': self.x_axis_name, 'y_var_titles': self.y_var_titles,
                        'y_var_units': self.y_var_units, 'y_var_names': self.y_var_names,
                        'x_axis_type': self.x_axis_type, 'y_axis_title': self.y_axis_title,
                        'color_list': self.color_list, 'use_default_colors': self.use_default_colors,
                        'chart_3d': self.chart_3d, 'chart_data': self.chart_data}

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


def show_line_chart(request):
    data = FAKE_DATA
    print(data)
    y_var_names = ["myVar1", "myVar2"]
    y_var_titles = ["Var1", "Var2"]
    y_var_units = ["v1_unit", "v2_unit"]
    x_axis_type = "time"
    x_axis_name = "time"
    x_axis_title = "Time"
    x_axis_unit = ""
    y_axis_title = "Var"
    color_list_request = ['blue', 'red', 'green']
    use_default_colors = "false"
    chart_3d = "false"

    color_list = define_color_list(color_list_request)

    line_chart = XY_chart(request, x_axis_name, x_axis_title, x_axis_unit, y_var_names, y_var_titles, y_var_units,
                          x_axis_type, y_axis_title, data, color_list, use_default_colors, chart_3d, 'line_chart')
    return line_chart.show_chart()


def show_column_chart(request):
    data = COLUMNCHART_DATA
    print(data)
    y_var_names = ["year2017", "year2018"]
    y_var_titles = ["Year 2017", "Year 2018"]
    y_var_units = ["%", "%"]
    x_axis_type = "text"
    x_axis_name = "country"
    x_axis_title = "Country"
    x_axis_unit = ""
    y_axis_title = "GDP Rates"
    color_list_request = ['blue', 'red', 'green']
    use_default_colors = "false"
    chart_3d = "true"

    color_list = define_color_list(color_list_request)
    column_chart = XY_chart(request, x_axis_name, x_axis_title, x_axis_unit, y_var_names, y_var_titles, y_var_units,
                            x_axis_type, y_axis_title, data, color_list, use_default_colors, chart_3d, 'column_chart')
    return column_chart.show_chart()


def show_range_chart(request):
    data = FAKE_DATA
    y_var_names = ["myVar1", "myVar2"]
    y_var_titles = ["Var1", "Var2"]
    y_var_units = ["v1_unit", "v2_unit"]
    x_axis_type = "time"
    x_axis_name = "time"
    x_axis_title = "Time"
    x_axis_unit = ""
    y_axis_title = "Var"
    color_list_request = ['blue', 'red', 'green']
    use_default_colors = "true"
    chart_3d = "false"

    color_list = define_color_list(color_list_request)

    range_chart = XY_chart(request, x_axis_name, x_axis_title, x_axis_unit, y_var_names, y_var_titles, y_var_units,
                           x_axis_type, y_axis_title, data, color_list, use_default_colors, chart_3d, 'range_chart')
    return range_chart.show_chart()


def show_bar_range_chart(request):
    data = BAR_RANGE_CHART_DATA
    y_var_names = ["name"]
    y_var_titles = ["Var1", "Var2"]
    y_var_units = ["-"]
    x_axis_type = "time"
    x_axis_name = "time"
    x_axis_title = "Time"
    x_axis_unit = ""
    y_axis_title = "Name"
    color_list = []
    use_default_colors = "true"
    chart_3d = "false"
    bar_range_chart = XY_chart(request, x_axis_name, x_axis_title, x_axis_unit, y_var_names, y_var_titles, y_var_units,
                               x_axis_type, y_axis_title, data, color_list, use_default_colors, chart_3d, 'bar_range_chart')
    return bar_range_chart.show_chart()


def show_stacked_column_chart(request):
    data = COLUMNCHART_DATA
    print(data)
    y_var_names = ["year2017", "year2018"]
    y_var_titles = ["Year 2017", "Year 2018"]
    y_var_units = ["%", "%"]
    x_axis_type = "text"
    x_axis_name = "country"
    x_axis_title = "Country"
    x_axis_unit = ""
    y_axis_title = "GDP Rates"
    color_list_request = ['blue', 'red', 'green']
    use_default_colors = "false"
    chart_3d = "true"
    color_list = define_color_list(color_list_request)
    stacked_column_chart = XY_chart(request, x_axis_name, x_axis_title, x_axis_unit, y_var_names, y_var_titles, y_var_units,
                            x_axis_type, y_axis_title, data, color_list, use_default_colors, chart_3d, 'stacked_column_chart')

    return stacked_column_chart.show_chart()


def bar_heat_map(request):
    data = BAR_HEATMAP_DATA
    print(data)
    y_var_names = ["value"]
    y_var_titles = ["Value"]
    y_var_units = ["units"]
    x_axis_type = "text"
    x_axis_name = "category"
    x_axis_title = "Category"
    x_axis_unit = ""
    y_axis_title = "Value Units"
    color_list_request = "blue_red"
    use_default_colors = "false"
    chart_3d = "false"
    color_couple = AM_CHARTS_COLOR_HEATMAP_COUPLES[color_list_request]
    bar_heat_map_chart = XY_chart(request, x_axis_name, x_axis_title, x_axis_unit, y_var_names, y_var_titles,
                                    y_var_units,
                                    x_axis_type, y_axis_title, data, color_couple, use_default_colors, chart_3d,
                                    'bar_heat_map_chart')

    return bar_heat_map_chart.show_chart()

def sankey_diagram(request):
    return render(request, 'visualiser/sankey_diagram.html')


def chord_diagram(request):
    return render(request, 'visualiser/chord_diagram.html')


def heat_map(request):
    return render(request, 'visualiser/heat_map.html')



def horizontal_dumbbell(request):
    return render(request, 'visualiser/horizontal_dumbbell.html')


def multi_line_chart(request):
    return render(request, 'visualiser/multi_line_chart.html')


def line_chart_range(request):
    return render(request, 'visualiser/line_chart_range.html')


def line_chart_range2(request):
    return render(request, 'visualiser/line_chart_range2.html')



def define_color_list(color_list_request):
    color_list = []
    for color in color_list_request:
        color_list.append(AM_CHARTS_COLOR_INDEX_LIST[color])
    return color_list

