from random import randint, choice # Use it in function generate_data_for_heat_map

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

HEAT_MAP_COUNTRIES_CODES = [
                            'AF', 'AX', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT',
                            'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BQ', 'BA', 'BW',
                            'BV', 'BR', 'IO', 'BN', 'BG', 'BF', 'BI', 'KH', 'CM', 'CA', 'CV', 'KY', 'CF', 'TD', 'CL',
                            'CN', 'CX', 'CC', 'CO', 'KM', 'CG', 'CD', 'CK', 'CR', 'CI', 'HR', 'CU', 'CW', 'CY', 'CZ',
                            'DK', 'DJ', 'DM', 'DO', 'EC', 'EG', 'SV', 'GQ', 'ER', 'EE', 'ET', 'FK', 'FO', 'FJ', 'FI',
                            'FR', 'GF', 'PF', 'TF', 'GA', 'GM', 'GE', 'DE', 'GH', 'GI', 'GR', 'GL', 'GD', 'GP', 'GU',
                            'GT', 'GG', 'GN', 'GW', 'GY', 'HT', 'HM', 'VA', 'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IR',
                            'IQ', 'IE', 'IM', 'IL', 'IT', 'JM', 'JP', 'JE', 'JO', 'KZ', 'KE', 'KI', 'KP', 'KR', 'KW',
                            'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY', 'LI', 'LT', 'LU', 'MO', 'MK', 'MG', 'MW', 'MY',
                            'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'MX', 'FM', 'MD', 'MC', 'MN', 'ME', 'MS',
                            'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'NC', 'NZ', 'NI', 'NE', 'NG', 'NU', 'NF', 'MP',
                            'NO', 'OM', 'PK', 'PW', 'PS', 'PA', 'PG', 'PY', 'PE', 'PH', 'PN', 'PL', 'PT', 'PR', 'QA',
                            'RE', 'RO', 'RU', 'RW', 'BL', 'SH', 'KN', 'LC', 'MF', 'PM', 'VC', 'WS', 'SM', 'ST', 'SA',
                            'SN', 'RS', 'SC', 'SL', 'SG', 'SX', 'SK', 'SI', 'SB', 'SO', 'ZA', 'GS', 'SS', 'ES', 'LK',
                            'SD', 'SR', 'SJ', 'SZ', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH', 'TL', 'TG', 'TK', 'TO',
                            'TT', 'TN', 'TR', 'TM', 'TC', 'TV', 'UG', 'UA', 'AE', 'GB', 'US', 'UM', 'UY', 'UZ', 'VU',
                            'VE', 'VN', 'VG', 'VI', 'WF', 'EH', 'YE', 'ZM', 'ZW'
                        ]


def generate_data_for_heat_map():
    data = []
    for country in HEAT_MAP_COUNTRIES_CODES:
        data.append(
            {
                "id": country,
             "value": randint(1, 50)
             }
        )
    return data


def generate_data_for_heat_map_chart():
    models = ["ALADIN", "FORECAST", "JRC-EU-TIMES", "LEAP", "NEMESIS", "CONTO", "MARKAL-India", "MAPLE", "NATEM",
              "SISGEMA", "TIMES-CAC", "DICE", "GCAM", "ICES", "Gemini-E3", "TIAM", "MUSE", "42", "E3ME"]
    sdgs = ["Total", "by eductional attainment level", "by age", "by sex", "by econcomic activity",
            "(Partially) Aggregated (*)", "Macroeconomic", "Private Investments", "Public investments",
            "(Partially) Aggregated (*)", "Expenditures", "Receipts", "Social benefits", "Balances",
            "(Partially) Aggregated (*)", "Production", "Value added", "Imports", "Exports", "Employment",
            "Energy expenditure", "Investments", "Raw material consumption", "Other materials consumption",
            "(Partially) Aggregated (*)", "Total gross/real disposable income", "Capital incomes", "Labour incomes",
            "Social transfers", "By quantiles", "Energy poverty", "(Partially) Aggregated (*)"]
    data = []
    for model in models:
        for sdg in sdgs:
            data.append(
                {
                    "SDG": sdg,
                    "Model": model,
                    "value": randint(0, 2)
                }
            )
    return data


def generate_data_for_range_chart():
    vars = ["F", "BC", "NL", "C", "P"]
    data = []
    for k, var in enumerate(vars):
        for year in range(2010,2101):
            v = randint(-10, 10)
            multi_c = choice([-1, 1])
            v_c = v + multi_c * randint(0, 5)
            c_lose = v_c
            # v_p = randint((-2)*v, 2*v)
            multi_o = choice([-1, 1])
            v_p = v + multi_o * randint(0, 5)
            o_open = v_p
            data.append(
                {
                    var: v,
                    "close_"+str(k): c_lose,
                    "open_"+str(k): o_open,
                    "year_"+str(k): year
                }
            )
    return data



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

