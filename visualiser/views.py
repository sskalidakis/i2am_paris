from django.shortcuts import render

from django.http import HttpResponse

class XY_chart:
    def __init__(self, request, x_axis_name, x_axis_title, x_axis_unit, y_axis_name, y_axis_title, y_axis_unit, chart_data, chart_type):
        self.x_axis_name = x_axis_name
        self.x_axis_title = x_axis_title
        self.x_axis_unit = x_axis_unit
        self.y_axis_name = y_axis_name
        self.y_axis_title = y_axis_title
        self.y_axis_unit = y_axis_unit
        self.chart_data = chart_data
        self.request = request
        self.chart_type = chart_type

    def show_chart(self):
        if self.chart_type == 'line_chart':
            return render(self.request, 'visualiser/line_chart_am4.html',
                          {'x_axis_title': self.x_axis_title, 'x_axis_unit': self.x_axis_unit,
                           'x_axis_name': self.x_axis_name, 'y_axis_title': self.y_axis_title,
                           'y_axis_unit': self.y_axis_unit, 'y_axis_name': self.y_axis_name,
                           'chart_data': self.chart_data})
        elif self.chart_type == 'column_chart':
            return render(self.request, 'visualiser/column_chart_am4.html',
                          {'x_axis_title': self.x_axis_title, 'x_axis_unit': self.x_axis_unit,
                           'x_axis_name': self.x_axis_name, 'y_axis_title': self.y_axis_title,
                           'y_axis_unit': self.y_axis_unit, 'y_axis_name': self.y_axis_name,
                           'chart_data': self.chart_data})


def show_line_chart(request):
    line_chart = XY_chart(request, 'time', 'Time', '', 'visits', 'Visits', 'v_unit',{}, 'line_chart')
    return line_chart.show_chart()


def show_column_chart(request):
    column_chart = XY_chart(request, 'time', 'Time', '', 'visits', 'Visits', 'v_unit', {}, 'column_chart')
    return column_chart.show_chart()


def sankey_diagram(request):
    return render(request, 'visualiser/sankey_diagram.html')


def chord_diagram(request):
    return render(request, 'visualiser/chord_diagram.html')


def heat_map(request):
    return render(request, 'visualiser/heat_map.html')


def bar_heat_map(request):
    return render(request, 'visualiser/bar_heat_map.html')


def horizontal_dumbbell(request):
    return render(request, 'visualiser/horizontal_dumbbell.html')


def multi_line_chart(request):
    return render(request, 'visualiser/multi_line_chart.html')


def line_chart_range(request):
    return render(request, 'visualiser/line_chart_range.html')


# def show_line_chart2(request):
#     x_axis_name = 'time'
#     x_axis_title = 'Time'
#     x_axis_unit = ''
#     y_axis_name = 'visits'
#     y_axis_title = 'Visits'
#     y_axis_unit = 'v_unit'
#     chart_data = {}
#     return render(request, 'visualiser/line_chart_am4.html', {'x_axis_title':x_axis_title, 'x_axis_unit':x_axis_unit,
#                                                               'x_axis_name': x_axis_name, 'y_axis_title':y_axis_title,
#                                                               'y_axis_unit':y_axis_unit, 'y_axis_name': y_axis_name,
#                                                               'chart_data': chart_data})

