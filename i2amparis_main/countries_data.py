from i2amparis_main.models import *
import random




class RetriveDB:
    def __init__(self, model_name):
        # self.model_json = {}  # Create in method create_model_json
        self.model_name = model_name
        self.bool_dict = {
            'Endogenous': '#97ae21',
            'Exogenous': '#97ae21',
            'Not represented': 'grey'
        }
        models_lst = list(ModelsInfo.objects.values_list('model_name', flat=True))
        if self.model_name in models_lst:
            self.model_id = ModelsInfo.objects.get(model_name=self.model_name).id
        else:
            self.model_id = ModelsInfo.objects.all()[0].id
        self.retrieve_granularity = {
            'Sectors': self.retrieve_sectors(),
            'Emissions': self.retrieve_emission(),
            'Socioecons': self.retrieve_socioecon(),
            'Policy': self.retrieve_policy(),
            'Mitigation-Adaption measures': self.retrieve_mitigation_adaption(),
            'SDGs': self.retrieve_sdgs()
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
        # model_id = ModelsInfo.objects.filter(model_name=self.model_name)[0].id
        # TODO first we must check if there is a region for current model
        regions = Regions.objects.filter(model_name=self.model_id)
        data = []
        color_list = self.generate_colors(len(regions))
        for k, region in enumerate(regions):
            region_id = region.id
            region_name = region.region
            countries = Countries.objects.filter(model_name=self.model_id, region=region_id)
            # If the region name is the " " descr is the name of the country else we retrieve the description of
            # the specific region and set the field descr which will use in front- end to appear the tooltip when we
            # hover over the country-region
            if region_name == " ":
                region_name = "The region of " + self.model_name
                countries_list = list(map(lambda x: {"title": x.country_name, "id": x.country_code,
                                                     "descr": x.country_name}, countries))
            else:
                descr = Regions.objects.get(region=region_name).descr
                countries_list = list(map(lambda x: {"title": x.country_name, "id": x.country_code,
                                                     "descr": descr}, countries))
            temp = {
                "name": region_name,
                "color": color_list[k],
                "data": countries_list
            }
            data.append(temp)
        return data

    def retrieve_sectors(self):
        """
          d=Sectors.objects.values_list('name',flat=True).distinct()
        :return:
        """
        subcategories = {
            "Energy sources": "Commodities / Sources",
            "Energy transformation": "Transformation sectors",
            "Energy storage": "Storage"
        }
        categories = {
            "Industry": "Industry (energy demand/economic output)",
            "Buildings": "Buildings",
            "Agriculture, Forestry, Land Use (AFOLU)": "AFOLU"
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
            subcategories = list(Sectors.objects.
                                 filter(category=temp).values_list('subcategory', flat=True).distinct())
            for j in subcategories:
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
            True: '#97ae21',
            False: 'gray'
        }
        sectors_dict_html = {}
        # Because the sector_cat_dict and sector_sub_dict haven't sub categories we treat them the same
        sectors_cat_dict.update(sectors_sub_dict)
        for i in sectors_cat_dict:
            temp_lst = []
            for j in sectors_cat_dict[i]:
                [[k, v]] = j.items()
                temp_lst.append(' <li> <font color = "{}" >{} </font> </li> '.format(color_dict[v], k))
            sectors_dict_html[i] = self.is_enable_category('<ul> {} </ul>'.format(''.join(temp_lst)), cat=i)
        # Category Transportation has sub categories so we should create a nested list
        transportations = []
        for i in sectors_cat_dict2:
            temp = []
            for j in sectors_cat_dict2[i]:
                [[k, v]] = j.items()
                temp.append(' <li> <font color = "{}" >{} </font> </li> '.format(color_dict[v], k))
            temp = '<li> {} <ul> {} </ul></li>'.format(i, ''.join(temp))
            transportations.append(temp)
        transportations = '<ul> {} </ul>'.format(''.join(transportations))
        sectors_dict_html.update({
            'Transportation': self.is_enable_category(transportations, cat='Transportation')
        })
        # TODO generate the tooltip. Take the keys from the sectors_dict_html and generate the categories
        # TODO return sectors_dict_html
        # TODO check the name for AFOLU
        return sectors_dict_html

    def retrieve_socioecon(self):
        """
        Retrieve and generate the html code for Socioecon. Granularity

        :return:
        """
        # bool_dict = {
        #     'Endogenous': '#97ae21',
        #     'Exogenous': '#97ae21',
        #     'Not represented': 'grey'
        # }
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
            temp = list(map(lambda x: '<li> <font color = "{}" >{} </font> </li> '.format(self.bool_dict[x[0]], x[1])
                            , socioecons_dict[i]))
            temp = '<ul> {} </ul>'.format(''.join(temp))
            socioecons_html.update({
                i: self.is_enable_category(temp, cat=i)
            })
        return socioecons_html

    def retrieve_emission(self):
        """

        :return: A dict with keys the name of emissions, such as CO2 and value the is Endogenous or Exogenous
        """
        categories = list(Emissions.objects.values_list('categories', flat=True).distinct())
        emission_html = {}
        for i in categories:
            temp = \
                list(Emissions.objects.filter(categories=i, model_name=
                self.model_id).values_list('name', 'state').distinct())
            temp = list(filter(lambda y: y[1]!= 'Not represented', temp))
            for j in temp:
                emission_html.update({
                    j[0]: {'html': j[1]}
                })
        #     temp = list(
        #         map(lambda x: '<li> <font color = "{}" >{} </font> </li> '.format(self.bool_dict[x[1]], x[0]), temp))
        #     temp = '<ul> {} </ul>'.format(''.join(temp))
        #     emission_html.update({
        #         i: self.is_enable_category(temp)
        #     })
        return emission_html

    def retrieve_policy(self):
        """

        :return:
        """
        bool_dict = {
            'Feasible': '#97ae21',
            'Feasible with modifications': '#97ae21',
            'Not feasible': 'grey'
        }
        categories = list(Policies.objects.values_list('category', flat=True).distinct())
        policies_html = {}
        for i in categories:
            temp = list(Policies.objects.filter(category=i, model_name=self.model_id).
                        values_list('name', 'state').distinct())
            temp = list(
                map(lambda x: '<li> <font color = "{}" >{} </font> </li> '.format(bool_dict[x[1]], x[0]), temp))
            temp = '<ul> {} </ul>'.format(''.join(temp))
            policies_html.update({
                i: self.is_enable_category(temp, cat=i)
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
        behavior_lst = list(filter(lambda x: 'BEHAVIOUR' in x.upper(),
                                   list(Mitigations.objects.values_list('subcategory', flat=True).distinct())))
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
                mitigation_adaption_dict.update({
                    j: self.is_enable_category(self.create_html_lists(
                        list(map(lambda x: {x: True} if x in temp_true else {x: False}, temp_all))), cat=j)
                })
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
            mitigation_adaption_dict.update({
                i: self.is_enable_category(self.create_html_lists(temp_dict, is_nested=True), cat=i)
            })
        temp_all = list(Mitigations.objects.filter(category='LULUCF').values_list('name', flat=True).distinct())
        temp_true = list(Mitigations.objects.filter(category='LULUCF', model_name=self.model_id)
                         .values_list('name', flat=True).distinct())
        mitigation_adaption_dict.update({
            'LULUCF': self.is_enable_category(
                self.create_html_lists(list(map(lambda x: {x: True} if x in temp_true else {x: False}, temp_all))),
                cat='LULUCF')
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
        mitigation_adaption_dict.update({
            'Adaptation': self.is_enable_category(self.create_html_lists(temp_dict, is_nested=True), cat='Adaptation')
        })
        temp = list(map(lambda x: {x: True} if Mitigations.objects.filter(subcategory=x,
                                                                          model_name=self.model_id).count() > 0
        else {x: False}, behavior_lst))
        mitigation_adaption_dict.update({
            'Behavioural changes': self.is_enable_category(self.create_html_lists(temp), cat='Behavioural changes')
        })
        return mitigation_adaption_dict

    def retrieve_sdgs(self):
        """
        Retrieve the sdgs for the given model

        :return: Dict with keys 7,9,12(are strings) and value html code with head the full name of sdg and a list of
        description
        """
        data = list(Sdgs.objects.filter(model_name=self.model_id).values_list('description', 'name'))
        sdgs_html = {}
        for descr,name in data:
            if '7' in name:
                temp = '7'
            elif '9' in name:
                temp = '9'
            elif '12' in name:
                temp = '12'
            temp_html = '<h3> {} </h3> <ul> <li> {} </li> </ul>'.format(name, descr)
            sdgs_html.update({
                temp: {'html':temp_html}
            })
        return sdgs_html



    def is_enable_category(self, html_code, cat):
        """

        :param html_code:
        :return:
        """
        bool_dict = {
            True: 'green',
            False: 'grey'
        }
        return {
            'html': '<h4> {} </h4> {}'.format(cat, html_code),
            'is_enable': bool_dict['#97ae21' in html_code]
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
        bool_dict = {
            True: '#97ae21',
            False: 'grey'
        }
        temp = list(map(lambda x: '<li> <font color = "{}" >{} </font> </li> '.format(
            bool_dict[x[1]], x[0]), data_tuple))
        temp = '<ul> {} </ul>'.format(''.join(temp))
        return temp

    # def retrive_granularity(self, granularity):
    #     """
    #     Abstract method which will place the granularity and will generate
    #     the html we want ( with this will manipulate and Mitigation- Adaption measures)
    #     Will we have a dictionary where we connect name with our db object, addtionaly each name of each granularity
    #     will have a icon this will be represented with the granularity_icon which will be a dict
    #
    #     :param granularity: sector, emission etc
    #     :return:
    #     """
    #     granularities_html = []
    #     # TODO add SDG
    #     granularity_dict ={
    #         "sectoral": Sectors,
    #         "emission": Emissions,
    #         "socioecon": Socioecons,
    #         "policy": Policies,
    #         "mitigation": Mitigations,
    #         "adaption": Adaptation
    #     }
    #
    #     granularities = granularity_dict[granularity]
    #     granularities_lst = list(set(map(lambda x: x.name, granularities.objects.all())))
    #     if self.model_name == '':
    #         for i in granularities_lst:
    #             granularities_html.append('<font color = "{}" >{} </font> '.format("red", i))
    #     else:
    #         model_granularities = list(map(lambda x: x.name, granularities.objects.filter(
    #             model_name=ModelsInfo.objects.filter(model_name=self.model_name)[0].id)))
    #         granularities_false = list(set(granularities_lst) - set(model_granularities))
    #         granularities_bool = {}
    #         for i in granularities_lst:
    #             if i in granularities_false:
    #                 # granularities_bool.update({
    #                 #     i: False
    #                 # })
    #                 granularities_html.append('<font color = "{}" >{} </font> '.format("red", i))
    #             else:
    #                 # granularities_bool.update({
    #                 #     i: True
    #                 # })
    #                 granularities_html.append('<font color = "{}" >{} </font> '.format("#97ae21", i))
    #     return " ".join(granularities_html)

    def create_models_btn(self):
        """
        Retrive all models names and create the buttons

        :return:
        """
        models_names = list(map(lambda x: x.model_name, ModelsInfo.objects.all()))
        return models_names
        # return " ".join(list(map(lambda x: '<a href="{}" >Model {}</a>'.format(x, x),  models_names)))

    def generate_colors(self, n):
        color_list = []
        for i in range(n):
            r = lambda: random.randint(0, 255)
            color_list.append('#%02X%02X%02X' % (r(), r(), r()))
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





