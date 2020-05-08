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

AM_CHARTS_COLOR_CODES_LIST = {
    "light_blue": "#65a5db",
    "blue": "#5079d4",
    "violet": "#8951db",
    "purple": "#7d3e9d",
    "fuchsia": "#a04293",
    "red": "#ad3741",
    "ceramic": "#a0432c",
    "light_brown": "#844b2c",
    "mustard": "#a78428",
    "gold": "#e6b323",
    "light_green": "#62993d",
    "green": "#3b6733",
    "cyan": "#4b9e91",
    "black": "#000000",
    "gray": "#b4b4b4",
    "white": "#FFFFFF"
}

AM_CHARTS_COLOR_HEATMAP_COUPLES = {
    "blue_red": ["#63a1db", "#a32f22"],
    "green_red": ["#66bd7d", "#a32f22"],
    "beige_purple": ["#f0d2bd", "#80308a"],
    "purple_orange": ["#f5d1ff", "#db6b21"],
    "cyan_green": ["#99c9c9", "#446614"],
    "yellow_gold": ["#f7ecc2", "#dba200"],
    "skin_red": ["#f7dfd0", "#8d1915"],
    "grey_darkblue": ["#eaecf7", "#1f3b5e"],
    "lightblue_green": ["#bbe1ff", "#2e5c20"]

}


D3_PARALLEL_COORDINATES_COLORS = [
                                     [185, 56, 73],
                                     [37, 50, 75],
                                     [325, 50, 39],
                                     [10, 28, 67],
                                     [271, 39, 57],
                                     [56, 58, 73],
                                     [28, 100, 52],
                                     [41, 75, 61],
                                     [60, 86, 61],
                                     [30, 100, 73],
                                     [318, 65, 67],
                                     [274, 30, 76],
                                     [20, 49, 49],
                                     [334, 80, 84],
                                     [185, 80, 45],
                                     [10, 30, 42],
                                     [339, 60, 49],
                                     [359, 69, 49],
                                     [204, 70, 41],
                                     [1, 100, 79],
                                     [189, 57, 75],
                                     [110, 57, 70],
                                     [214, 55, 79],
                                     [339, 60, 75],
                                     [120, 56, 40]
                    ]


def define_color_index_list(color_list_request):
    color_list = []
    for color in color_list_request:
        color_list.append(AM_CHARTS_COLOR_INDEX_LIST[color])
    return color_list


def define_color_code_list(color_list_request):
    color_list = []
    for color in color_list_request:
        if not AM_CHARTS_COLOR_CODES_LIST.get(color) is None:
            color_list.append(AM_CHARTS_COLOR_CODES_LIST[color])
    return color_list

