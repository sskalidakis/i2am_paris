from i2amparis_main.models import *
import random
from random import shuffle




class RetriveDB:
    def __init__(self, model_name):
        # self.model_json = {}  # Create in method create_model_json
        self.model_name = model_name
        self.bool_dict = {
            'Endogenous': 'green',
            'Exogenous': 'green',
            'Not represented': 'grey'
        }
        models_lst = list(ModelsInfo.objects.values_list('model_name', flat=True))
        if self.model_name in models_lst:
            self.model_id = ModelsInfo.objects.get(model_name=self.model_name).id
        else:
            self.model_id = ModelsInfo.objects.all().order_by('ordering')[0].id
        self.retrieve_granularity = {
            'Sectors': self.retrieve_sectors(),
            'Policy': self.retrieve_policy(),
            'SDGs': self.retrieve_sdgs(),
            'SocioEconomics': self.retrieve_socioecon(),
            'Emissions': self.retrieve_emission(),
            'MitigationAdaptationMeasures': self.retrieve_mitigation_adaption(),
        }

    def create_json(self):
        """
      Get the model_name and retrive countries from database
      and create the json which need the map to represent the
      countries
      We must have two case one where model haven't region and second where there are regions
      1) In first case each country is a 'group of countries', also the 'name' of the group will be the name of country
      2) In second case each region is a group of countries

      :param model_name:
      :return:
      """
        counter = 0
        data = []
        # First we take the list of region for the given model id
        regions = list(Regions.objects.filter(model_name=self.model_id).values_list('region_name', flat=True))
        color_list = self.generate_colors(len(regions))
        # Then loop in regions and get the countries, name and code of each one
        print (regions)
        for k,region in enumerate(regions):
            temp = Regions.objects.get(region_name=region)
            # Get the id of the region
            region_id = temp.id
            # Get the description of region
            region_descr = temp.descr
            countries_of_region = list(Countries.objects.filter(region_name=region_id).values_list(
                'country_name', 'country_code'))
            # Make a list which each element is a dict with keys tittle:<name of country>,id:<country code>,
            # descr:<descr of region>
            countries_list = list(map(lambda x: {'title': x[0], 'id': x[-1], 'descr': region_descr},
                                      countries_of_region))
            if len(countries_list) == 1:
                selected_color = color_list[0]
                print('!!region has one country!!')
            else:
                counter = counter + 1
                selected_color = color_list[counter]
            temp_dict = {
                "name": temp.region_title,
                "color": selected_color,
                "data": countries_list
            }
            data.append(temp_dict)
        return data
        #
        #
        # # model_id = ModelsInfo.objects.filter(model_name=self.model_name)[0].id
        # # TODO first we must check if there is a region for current model
        # regions = Regions.objects.filter(model_name=self.model_id)
        # data = []
        # color_list = self.generate_colors(len(regions))
        # for k, region in enumerate(regions):
        #     region_id = region.id
        #     region_name = region.region
        #     countries = Countries.objects.filter(model_name=self.model_id, region=region_id)
        #     # If the region name is the " " descr is the name of the country else we retrieve the description of
        #     # the specific region and set the field descr which will use in front- end to appear the tooltip when we
        #     # hover over the country-region
        #     if region_name == " ":
        #         region_name = "The region of " + self.model_name
        #         countries_list = list(map(lambda x: {"title": x.country_name, "id": x.country_code,
        #                                              "descr": x.country_name}, countries))
        #     else:
        #         descr = Regions.objects.get(region=region_name).descr
        #         countries_list = list(map(lambda x: {"title": x.country_name, "id": x.country_code,
        #                                              "descr": descr}, countries))
        #     temp = {
        #         "name": region_name,
        #         "color": color_list[k],
        #         "data": countries_list
        #     }
        #     data.append(temp)
        # return data

    def retrieve_sectors(self):
        """
          d=Sectors.objects.values_list('name',flat=True).distinct()
        :return:
        """
        green_color = '#97ae21'
        subcategories = {
            "Energy sources": "Commodities / Sources",
            "Energy transformation": "Transformation sectors",
            "Energy storage": "Storage"
        }
        categories = {
            "Industry": "Industry (energy demand/economic output)",
            "Buildings": "Buildings",
            "Agriculture, Forestry, Land Use(AFOLU)": "AFOLU"
        }
        categories2 = {
            "Transportation": "Transportation"
        }
        sectors_sub_dict = {}
        for i in subcategories:
            temp = subcategories[i]
            temp_lst = list(Sectors.objects.filter(subcategory=temp).values_list('name', flat=True).distinct())
            if self.model_name == '':
                temp_lst = list(map(lambda x: {x: False}, temp_lst))
            else:
                temp_lst = list(map(lambda x: {
                    x: Sectors.objects.filter(name=x, subcategory=temp, model_name=self.model_id).count() > 0},
                                    temp_lst))
            sectors_sub_dict.update({
                # i: list(Sectors.objects.filter(subcategory=subcategories[i]).values_list('name', flat=True).distinct())
                i: temp_lst
            })
        sectors_cat_dict = {}
        for i in categories:
            temp = categories[i]
            temp_lst = list(Sectors.objects.filter(category=temp).values_list('name', flat=True).distinct())
            if self.model_name == '':
                temp_lst = list(map(lambda x: {x: False}, temp_lst))
            else:
                temp_lst = list(map(
                    lambda x: {x: Sectors.objects.filter(name=x, category=temp, model_name=self.model_id).count() > 0},
                    temp_lst))

            sectors_cat_dict.update({
                # i: list(Sectors.objects.filter(category=categories[i]).values_list('name', flat=True).distinct())
                i: temp_lst
            })
        sectors_cat_dict2 = {}
        for i in categories2:
            temp = categories2[i]
            subcategories2 = list(Sectors.objects.
                                 filter(category=temp).values_list('subcategory', flat=True).distinct())
            for j in subcategories2:
                temp_lst = list(Sectors.objects.filter(subcategory=j).values_list('name', flat=True).distinct())
                if self.model_name == '':
                    temp_lst = list(map(lambda x: {x: False}, temp_lst))
                else:
                    temp_lst = list(map(lambda x: {
                        x: Sectors.objects.filter(subcategory=j, name=x, model_name=self.model_id).count() > 0},
                                        temp_lst))
                sectors_cat_dict2.update({
                    # j: list(Sectors.objects.filter(subcategory=j).values_list('name', flat=True).distinct())
                    j: temp_lst
                })
        color_dict = {
            True: green_color,
            False: 'grey'
        }
        bool_dict_decor = {
            True: 'none',
            False: 'line-through'
        }
        sectors_dict_html = {}
        # Because the sector_cat_dict and sector_sub_dict haven't sub categories we treat them the same
        sectors_cat_dict.update(sectors_sub_dict)
        for i in sectors_cat_dict:
            temp_lst = []
            for j in sectors_cat_dict[i]:
                [[k, v]] = j.items()
                temp_lst.append(' <li style="color:{};text-decoration:{}">{} </li> '.format(color_dict[v],bool_dict_decor[v], k))
            # sectors_dict_html[i] = self.is_enable_category('<ul> {} </ul>'.format(''.join(temp_lst)), cat=i)
            temp_dict = self.is_enable_category('<ul> {} </ul>'.format(''.join(temp_lst)), cat=i)
            temp_html = temp_dict['html']
            temp_is_enable = temp_dict['is_enable']

            if i in categories:
                icon = Sectors.objects.filter(category=categories[i])[0].icon
            else:
                icon = Sectors.objects.filter(subcategory=subcategories[i])[0].icon
            sectors_dict_html[i] = {
                'html': temp_html,
                'is_enable': temp_is_enable,
                'icon': icon
            }
        # Category Transportation has sub categories so we should create a nested list
        transportations = []
        for i in sectors_cat_dict2:
            temp = []
            for j in sectors_cat_dict2[i]:
                [[k, v]] = j.items()
                temp.append('<li style="color:{};text-decoration:{}">{}</li>'.format(color_dict[v],
                                                                                        bool_dict_decor[v], k))
            temp = '<li> {} <ul> {} </ul></li>'.format(i, ''.join(temp))
            transportations.append(temp)
        transportations = '<ul> {} </ul>'.format(''.join(transportations))
        # sectors_dict_html.update({
        #     'Transportation': self.is_enable_category(transportations, cat='Transportation')
        # })
        temp_dict = self.is_enable_category(transportations, cat='Transportation')
        temp_html = temp_dict['html']
        temp_is_enable = temp_dict['is_enable']
        icon = Sectors.objects.filter(category='Transportation')[0].icon
        sectors_dict_html['Transportation']={
            'html': temp_html,
            'is_enable': temp_is_enable,
            'icon': icon
        }
        # TODO generate the tooltip. Take the keys from the sectors_dict_html and generate the categories
        # TODO return sectors_dict_html
        # TODO check the name for AFOLU
        return sectors_dict_html

    def retrieve_socioecon(self):
        """
        Retrieve and generate the html code for Socioecon. Granularity

        :return:
        """
        green_color = '#97ae21'
        bool_dict = {
            'Endogenous': green_color,
            'Exogenous': green_color,
            'Not represented': 'grey'
        }
        bool_dict_decor = {
            'Endogenous': 'none',
            'Exogenous': 'none',
            'Not represented': 'line-through'
        }

        category = ['Demography']
        category2 = list(Socioecons.objects.values_list('subcategory', flat=True).distinct())
        category2 = list(filter(lambda x: x != ' ', category2))
        category1_dict = {
            category[0]: list(Socioecons.objects.filter(model_name=self.model_id, category=category[0]).
                              values_list('state', 'name').distinct())}
        category2_dict = {}
        for i in category2:
            category2_dict.update({
                i: list(Socioecons.objects.filter(model_name=self.model_id, subcategory=i).
                        values_list('state', 'name').distinct())})
        socioecons_dict = {}
        socioecons_dict.update(category1_dict)
        socioecons_dict.update(category2_dict)
        socioecons_html = {}
        for i in socioecons_dict:
            temp = list(map(lambda x: '<li style="color:{};text-decoration:{}"> {} </li> '.format(bool_dict[x[0]],bool_dict_decor[x[0]], x[1]), socioecons_dict[i]))
            temp = '<ul> {} </ul>'.format(''.join(temp))
            # socioecons_html.update({
            #     i: self.is_enable_category(temp, cat=i)
            # })
            bool_dict2 = {
                True: 'green',
                False: 'grey'
            }
            socioecons_html.update(({
                    i: {
                        'html': '<h4 style="text-align:center;padding:5px;margin-bottom:5px"> {} </h4> {}'.format(i,
                                                                                                                  temp),
                        'is_enable': bool_dict2[green_color in temp],
                        'icon': Socioecons.objects.filter(subcategory=i)[0].icon}
            }))
        return socioecons_html

    def retrieve_emission(self):
        categories = list(Emissions.objects.values_list('categories', flat=True).distinct())
        emission_html = {}
        for category in categories:
            category_emissions = (Emissions.objects.filter(categories=category, model_name=
            self.model_id).order_by('name').distinct())
            for emission in category_emissions:
                if emission.state != 'Not represented':
                    is_enabled = 'green'
                else:
                    is_enabled = 'grey'
                emission_html[emission.name] = {'html':'<h4 style="text-align:center">' + emission.title + '</h4><p  style="text-align:center">'+ emission.state + '</p>','is_enable': is_enabled, 'icon':emission.icon}


        """

        :return: A dict with keys the name of emissions, such as CO2 and value the is Endogenous or Exogenous
        """
        # categories = list(Emissions.objects.values_list('categories', flat=True).distinct())
        # emission_html = {}
        # for i in categories:
        #     temp = \
        #         list(Emissions.objects.filter(categories=i, model_name=
        #         self.model_id).values_list('name', 'state').distinct())
        #     temp = list(filter(lambda y: y[1] != 'Not represented', temp))
        #     for j in temp:
        #         emission_html.update({
        #             j[0]: {'html': j[1], 'is_enable': 'green'}
        #         })
        # emission_true = list(emission_html.keys())
        # emission_all = list(Emissions.objects.all().values_list('name', flat=True).distinct())
        # for i in emission_all:
        #     if i not in emission_true:
        #         emission_html.update({
        #             i: {'html': ' ', 'is_enable': 'grey'}
        #         })

        return emission_html

    def retrieve_policy(self):
        """

        :return:
        """
        green_color =  '#97ae21'
        bool_dict = {
            'Feasible': green_color,
            'Feasible with modifications': green_color,
            'Not feasible': 'grey'
        }
        bool_dict_decor = {
            'Feasible': 'none',
            'Feasible with modifications': 'none',
            'Not feasible': 'line-through'
        }
        categories = list(Policies.objects.values_list('category', flat=True).distinct())
        policies_html = {}
        for i in categories:
            temp = list(Policies.objects.filter(category=i, model_name=self.model_id).
                        values_list('name', 'state').distinct())
            temp = list(
                map(lambda x: '<li style="color:{};text-decoration:{}">{} </li> '.format(bool_dict[x[1]],bool_dict_decor[x[1]], x[0]), temp))
            temp = '<ul> {} </ul>'.format(''.join(temp))

            bool_dict2 = {
                True: 'green',
                False: 'grey'
            }

            policies_html.update({
                i: {
                    'html': '<h4 style="text-align:center;padding:5px;margin-bottom:5px"> {} </h4> {}'.format(i,
                                                                                                              temp),
                    'is_enable': bool_dict2[green_color in temp],
                    'icon': Policies.objects.filter(category=i)[0].icon}
            })
        return policies_html

    def retrieve_mitigation_adaption(self):
        """
        Retrieve the Mitigation-Adaption measures

        :return:
        """
        # TODO make a method which will take as arument a dictionary and another param if list is netsed or not,
        #  will generate html list
        categories_mitgation = list(Mitigations.objects.values_list('category', flat=True).distinct())
        behavior_lst = list(Mitigations.objects.filter(category='Behavioural Changes').values_list('subcategory', flat=True).distinct())
        mitigation_adaption_dict = {}
        # Manipulate the first 3 categories, where we use the subcategories
        for i in categories_mitgation[:3]:
            temp_sub = list(Mitigations.objects.filter(category=i).values_list('subcategory', flat=True).distinct())
            temp_sub = list(set(temp_sub) - set(behavior_lst))
            for j in temp_sub:
                temp_all = list(
                    Mitigations.objects.filter(subcategory=j, category=i).values_list('name', flat=True).distinct())
                temp_true = list(Mitigations.objects.filter(subcategory=j,
                                                            category=i, model_name=self.model_id).values_list(
                    'name', flat=True).distinct())
                temp_dict = self.is_enable_category(self.create_html_lists(
                    list(map(lambda x: {x: True} if x in temp_true else {x: False}, temp_all))), cat=j)
                temp_is_enable = temp_dict['is_enable']
                temp_html = temp_dict['html']
                icon = Mitigations.objects.filter(subcategory=j)[0].icon
                mitigation_adaption_dict.update({
                    j: {
                        'html': temp_html,
                        'is_enable': temp_is_enable,
                        'icon': icon
                    }
                })
                # mitigation_adaption_dict.update({
                #     j: self.is_enable_category(self.create_html_lists(
                #         list(map(lambda x: {x: True} if x in temp_true else {x: False}, temp_all))), cat=j)
                # })
        for i in categories_mitgation[3:-1]:
            sub_categories = list(
                Mitigations.objects.filter(category=i).values_list('subcategory', flat=True).distinct())
            sub_categories = list(set(sub_categories) - set(behavior_lst))
            temp_dict = {}
            for j in sub_categories:
                temp_all = list(Mitigations.objects.filter(category=i, subcategory=j)
                                .values_list('name', flat=True).distinct())
                temp_true = list(Mitigations.objects.filter(category=i, subcategory=j, model_name=self.model_id)
                                 .values_list('name', flat=True).distinct())
                temp_dict.update({
                    j: list(map(lambda x: {x: True} if x in temp_true else {x: False}, temp_all))
                })

            temp_dict = self.is_enable_category(self.create_html_lists(
                list(map(lambda x: {x: True} if x in temp_true else {x: False}, temp_all))), cat=j)
            temp_is_enable = temp_dict['is_enable']
            temp_html = temp_dict['html']
            icon = Mitigations.objects.filter(category=i)[0].icon
            mitigation_adaption_dict.update({
                i: {
                    'html': temp_html,
                    'is_enable': temp_is_enable,
                    'icon': icon
                }
            })
            # mitigation_adaption_dict.update({
            #     i: self.is_enable_category(self.create_html_lists(temp_dict, is_nested=True), cat=i)
            # })
        temp_all = list(Mitigations.objects.filter(category='LULUCF').values_list('name', flat=True).distinct())
        temp_true = list(Mitigations.objects.filter(category='LULUCF', model_name=self.model_id)
                         .values_list('name', flat=True).distinct())
        # mitigation_adaption_dict.update({
        #     'LULUCF': self.is_enable_category(
        #         self.create_html_lists(list(map(lambda x: {x: True} if x in temp_true else {x: False}, temp_all))),
        #         cat='LULUCF')
        # })
        temp_dict = self.is_enable_category(self.create_html_lists(
            list(map(lambda x: {x: True} if x in temp_true else {x: False}, temp_all))), cat='LULUCF')
        temp_is_enable = temp_dict['is_enable']
        temp_html = temp_dict['html']
        icon = Mitigations.objects.filter(category='LULUCF')[0].icon
        mitigation_adaption_dict.update({
            'LULUCF': {
                'html': temp_html,
                'is_enable': temp_is_enable,
                'icon': icon
            }
        })
        adaptation_sub = list(Adaptation.objects.values_list('category', flat=True).distinct())
        temp_dict = {}
        for i in adaptation_sub:
            temp_all = list(Adaptation.objects.filter(category=i).values_list('name', flat=True).distinct())
            temp_true = list(Adaptation.objects.filter(category=i, model_name=self.model_id)
                             .values_list('name', flat=True).distinct())
            temp_dict.update({
                i: list(map(lambda x: {x: True} if x in temp_true else {x: False}, temp_all))
            })
        # mitigation_adaption_dict.update({
        #     'Adaptation': self.is_enable_category(self.create_html_lists(temp_dict, is_nested=True), cat='Adaptation')
        # })
        temp_dict = self.is_enable_category(self.create_html_lists(
            list(map(lambda x: {x: True} if x in temp_true else {x: False}, temp_all))), cat='Adaptation')
        temp_is_enable = temp_dict['is_enable']
        temp_html = temp_dict['html']
        icon = Adaptation.objects.all()[0].icon
        mitigation_adaption_dict.update({
            'Adaptation': {
                'html': temp_html,
                'is_enable': temp_is_enable,
                'icon': icon
            }
        })
        temp = list(map(lambda x: {x: True} if Mitigations.objects.filter(subcategory=x,
                                                                          model_name=self.model_id).count() > 0
        else {x: False}, behavior_lst))
        temp_dict = self.is_enable_category(self.create_html_lists(temp), cat='Behavioural changes')
        temp_is_enable = temp_dict['is_enable']
        temp_html = temp_dict['html']
        icon = Mitigations.objects.filter(subcategory=behavior_lst[0])[0].icon
        mitigation_adaption_dict.update({
            'Behavioural changes': {
                'html': temp_html,
                'is_enable': temp_is_enable,
                'icon': icon
            }
        })
        # mitigation_adaption_dict.update({
        #     'Behavioural changes': self.is_enable_category(self.create_html_lists(temp), cat='Behavioural changes')
        # })
        return mitigation_adaption_dict

    def retrieve_sdgs(self):
        """
        Retrieve the sdgs for the given model

        :return: Dict with keys 7,9,12(are strings) and value html code with head the full name of sdg and a list of
        description
        """

        sdgs_all = Sdgs.objects.values_list('name',flat=True).distinct()
        sdgs_valid = Sdgs.objects.filter(model_name=self.model_id)
        sdgs_html = {}
        for sdg in sdgs_all:
            element = sdgs_valid.filter(name=sdg)
            if len(element)>0:
                is_enabled = 'green'
                sdgs_html[element[0].name] = {
                    'html': '<h4 style="padding:5px;margin-bottom:5px"> {}</h4>  <p style="margin-left:1em">{}</p> '.format(
                        element[0].title, element[0].description), 'is_enable': is_enabled,
                                                'icon': element[0].icon}
            else:
                is_enabled = 'grey'
                sdgs_html[sdg] = {
                    'html': '', 'is_enable': is_enabled,
                    'icon': Sdgs.objects.filter(name=sdg)[0].icon}




        # # Get all names of sdgs
        # data_all = list(Sdgs.objects.all().values_list('name', flat=True).distinct())
        # data = list(Sdgs.objects.filter(model_name=self.model_id).values_list('description', 'name'))
        # # Get a list of name of sdgs which is enable for a specific model
        # data_name_true = list(map(lambda x: x[1], data))
        # sdgs_html = {}
        # for descr, name in data:
        #     title = name
        #     name = [t for t in name if t.isdigit()][0]
        #     temp_html = '<h4 style="text-align:center;padding:5px;margin-bottom:5px"> <p>{}</p> </h4>  {} '.format(title, descr)
        #     sdgs_html.update({
        #         name: {'html': temp_html, 'is_enable': 'green', 'title':title}
        #     })
        # for i in data_all:
        #     if i not in data_name_true:
        #         # All the name have one digit, names are numbers for 1 to 16
        #         name = [t for t in i if t.isdigit()][0]
        #         sdgs_html.update({
        #             name: {'html': ' ', 'is_enable': 'grey'}
        #         })

        return sdgs_html

    def is_enable_category(self, html_code, cat):
        """

        :param html_code:
        :return:
        """
        green_color =  '#97ae21'
        bool_dict = {
            True: 'green',
            False: 'grey'
        }

        return {
            'html': '<h4 style="text-align:center;padding:5px;margin-bottom:5px"> {} </h4> {}'.format(cat, html_code),
            'is_enable': bool_dict[green_color in html_code],
        }

    def create_html_lists(self, data, is_nested=False):
        """
        Take a dict and create html lists

        :param is_nested:
        :param data:
        :return:
        """
        if is_nested:
            temp = []
            for i in data:
                temp.append('<li> {} {} </li>'.format(i, self.create_simple_list(self.create_data_tuple(data[i]))))
            res = '<ul> {} </ul>'.format(''.join(temp))
        else:
            res = self.create_simple_list(self.create_data_tuple(data))
        return res

    def create_data_tuple(self, data):
        """

        :param data:
        :return:
        """
        data_tuple = []
        for i in data:
            [[k, v]] = i.items()
            data_tuple.append((k, v))
        return data_tuple

    def create_simple_list(self, data_tuple):
        """

        :param data_tuple:
        :return:
        """
        green_color = '#97ae21'
        bool_dict = {
            True: green_color,
            False: 'grey'
        }
        bool_dict_decor = {
            True: 'none',
            False: 'line-through'
        }
        temp = list(map(lambda x: '<li style="color:{}; text-decoration:{}"> {} </li> '.format(
            bool_dict[x[1]],bool_dict_decor[x[1]], x[0]), data_tuple))
        temp = '<ul> {} </ul>'.format(''.join(temp))
        return temp

    def create_models_btn(self):
        """
        Retrive all models names and create the buttons

        :return:
        """
        # models_names = list(map(lambda x: x.model_name, ModelsInfo.objects.all()))
        # models_descriptions = list(map(lambda x: x.model_descr, ModelsInfo.objects.all()))
        # Get all table of models
        models_data = ModelsInfo.objects.all().order_by('ordering')
        # Get the titles of each model
        model_dict = {}
        for el in models_data:
            new_dict = {}
            new_dict['description'] = el.short_description
            new_dict['icon'] = el.icon
            new_dict['title'] = el.model_title
            new_dict['long_title'] = el.long_title
            model_dict[el.model_name] = new_dict
        return model_dict

    def generate_colors(self, n):
        color_list = []
        # color_list = ['#eef2c0','#ffdeb3','#b6f3fb','#d9d9d9','#e2e995','#ffc880','#85ebf9','#bfbfbf',
        #               '#d6e06b','#ffb14d','#55e4f7','#a6a6a6','#cbd741','#ff9b1a','#24dcf4','#8c8c8c',
        #               '#b1be28','#e68200','#0bc2db','#737373','#8a941f','#b36500','#0897aa','#595959',
        #               '#626a16','#804800','#066c7a','#404040','#3b3f0d','#4d2b00','#044149','#262626','#0d0d0d',
        #               ]
        color_list = ['#8a941f',  '#e68200', '#066c7a',
                      '#c7c78a','#91bec4','#ffb049','#0aaec5'
                      ,'#454a0f','#ab6100', '#033a42','#758000','#434747', '#26909e', '#a89172', '#8fbec4', '#a89fc9',
                      '#5a5275'
                      ]
        # shuffle(color_list)
        color_list = color_list
        # for i in range(n):
        #     r = lambda: random.randint(0, 255)
        #     color_list.append('#%02X%02X%02X' % (r(), r(), r()))

        return color_list

    def create_model_json(self):
        """
        Create the self.model_json,
        The model_json is a dict with keys the names of models and value  a dict with two keys
        descr, which include the description of model  and
        heading, which for now is remain empty

        :return:
        """
        data = list(ModelsInfo.objects.all().values_list('model_name', 'model_descr'))
        data = list(map(lambda x: {x[0], {'descr': x[1], 'heading': ''}}, data))
        return dict(j for i in data for j in i.items())





