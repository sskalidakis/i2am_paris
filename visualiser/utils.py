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
    "light_blue": "#539AD6",
    "blue": "#3869D6",
    "violet": "#7533D6",
    "purple": "#7B2CA2",
    "fuchsia": "#942A7C",
    "red": "#AA1C28",
    "ceramic": "#9c3421",
    "light_brown": "#843E1F",
    "mustard": "#c49d00",
    "gold": "#e6ac00",
    "light_green": "#5A992E",
    "green": "#26671E",
    "cyan": "#2c9e95",
    "black": "#000000",
    "gray": "#DDDDDD",
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

