from django.db import models

# Create your models here.
"""
Info:
Regional Granularity is separated in two tables-classes, Regions & Countries
Mitigation-Adaptation is separated in two tables-classes, Mitigation & Adaptation
In classes Emissions, Socioecons & Policies there is the field state which can have only three values,
* endogenous
* exogenous
* Not represented 
"""


class ModelsInfo(models.Model):
    """
    Tab Model information

    """
    model_name = models.TextField()
    model_title = models.TextField(default="")
    long_title = models.TextField(default="")
    partener = models.TextField()
    type_of_model = models.TextField()
    time_horizon = models.IntegerField()
    time_steps_in_solution = models.IntegerField(default=0)
    long_description = models.TextField()
    short_description = models.TextField(default="")
    icon = models.TextField(default="")
    ordering = models.IntegerField(default=0)
    coverage = models.TextField(default="")


    def __str__(self):
        return self.model_name


# class Sectors(models.Model):
#     """
#     Tab Sectoral Granularity
#
#     """
#     category = models.TextField()
#     subcategory = models.TextField(default="")
#     name = models.TextField()
#     icon = models.TextField(default="")
#     model_name = models.ManyToManyField(ModelsInfo)
#
#     def __str__(self):
#         return self.name
#
#
# class Emissions(models.Model):
#     """
#     Tab Emission Granularity
#
#     """
#     categories = models.TextField()  # TODO change the name to category
#     name = models.TextField()
#     state = models.TextField()
#     icon = models.TextField(default="")
#     model_name = models.ManyToManyField(ModelsInfo)
#     title = models.TextField(default="")
#
#     def __str__(self):
#         return self.name
#
#
# class Socioecons(models.Model):
#     """
#     Tab Socioecons Granularity
#
#     """
#     category = models.TextField()
#     subcategory = models.TextField(default="")
#     name = models.TextField()
#     state = models.TextField()
#     icon = models.TextField(default="")
#     model_name = models.ManyToManyField(ModelsInfo)
#
#     def __str__(self):
#         return self.name
#
#
# class Policies(models.Model):
#     """
#     Tab Policy Granularity
#
#     """
#     category = models.TextField()
#     name = models.TextField()
#     state = models.TextField()
#     icon = models.TextField(default="")
#     model_name = models.ManyToManyField(ModelsInfo)
#
#     def __str__(self):
#         return self.name


class Regions(models.Model):
    """
    Tab Regional Granularity(1)

    """
    region_name = models.TextField()
    region_title = models.TextField(default="")
    descr = models.TextField(default="")
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.region_name


class Countries(models.Model):
    """
    Tab Regional Granularity(2)

    """
    country_name = models.TextField()
    country_code = models.CharField(max_length=3)
    region_name = models.ManyToManyField(Regions)
    # model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.country_name


# class Mitigations(models.Model):
#     """
#     Tab Mitigation-Adaptation measures(1)
#
#     """
#     category = models.TextField()
#     subcategory = models.TextField(default="")
#     name = models.TextField()
#     icon = models.TextField(default="")
#     model_name = models.ManyToManyField(ModelsInfo)
#
#     def __str__(self):
#         return self.name
#
#
# class Adaptation(models.Model):
#     """
#     Tab Mitigation-Adaptation measures(2)
#
#     """
#     category = models.TextField()
#     name = models.TextField()
#     icon = models.TextField(default="")
#     model_name = models.ManyToManyField(ModelsInfo)
#
#     def __str__(self):
#         return self.name
#
#
# class Sdgs(models.Model):
#     """
#     Tab SDG Granularity
#
#     """
#     name = models.TextField()
#     title = models.TextField(default="")
#     description = models.TextField()
#     icon = models.TextField(default="")
#     model_name = models.ManyToManyField(ModelsInfo)
#
#     def __str__(self):
#         return self.name


class Feedback(models.Model):
    username = models.CharField(max_length=120)
    email = models.CharField(default='', max_length=120)
    subject = models.CharField(default='', max_length=120)
    message = models.TextField(default='')

    def __str__(self):
        return self.username


# ----------------------------------------------------------------------------------------------------------------------
# New models

class SdgsCat(models.Model):
    sdgs_cat = models.TextField()
    sdgs_title = models.TextField()
    ordering = models.IntegerField(default=0)
    model_id = models.ManyToManyField(ModelsInfo,
                                      through='SdgsName')
    ordering = models.IntegerField(default=0)


class SdgsName(models.Model):
    sdgs_cat_id = models.ForeignKey(SdgsCat,
                                    on_delete=models.CASCADE)
    model_id = models.ForeignKey(ModelsInfo,
                                 on_delete=models.CASCADE)
    sdgs_name = models.TextField()
    ordering = models.IntegerField(default=0)


class SdgsIcon(models.Model):
    sdgs_icon = models.TextField(default="")
    sdgs_cat_id = models.ManyToManyField(SdgsCat)


class AdaptationCat(models.Model):
    adaptation_cat = models.TextField()
    ordering = models.IntegerField(default=0)


class AdaptationName(models.Model):
    adaptation_name = models.TextField()
    adaptation_cat_id = models.ManyToManyField(AdaptationCat)
    model_id = models.ManyToManyField(ModelsInfo)
    ordering = models.IntegerField(default=0)


class AdaptationIcon(models.Model):
    adaptation_icon = models.TextField()
    adaptation_cat_id = models.ManyToManyField(AdaptationCat)


class MitigationsCat(models.Model):
    mitigations_cat = models.TextField()
    ordering = models.IntegerField(default=0)


class MitigationsSubCat(models.Model):
    mitigations_sub_cat = models.TextField(default="")
    mitigations_cat_id = models.ManyToManyField(MitigationsCat)
    ordering = models.IntegerField(default=0)


class MitigationsName(models.Model):
    mitigations_name = models.TextField()
    mitigations_sub_cat_id = models.ManyToManyField(MitigationsSubCat)
    model_id = models.ManyToManyField(ModelsInfo)
    ordering = models.IntegerField(default=0)


class MitigationsIcon(models.Model):
    mitigation_icon = models.TextField()
    mitigation_cat_id = models.ManyToManyField(MitigationsCat)


class SectorCat(models.Model):
    sector_cat = models.TextField()
    ordering = models.IntegerField(default=0)


class SectorSubCat(models.Model):
    sector_sub_cat = models.TextField(default="")
    sector_cat_id = models.ManyToManyField(SectorCat)
    ordering = models.IntegerField(default=0)


class SectorName(models.Model):
    sector_name = models.TextField()
    sector_sub_cat = models.ManyToManyField(SectorSubCat)
    model_id = models.ManyToManyField(ModelsInfo)
    ordering = models.IntegerField(default=0)


class SectorIcon(models.Model):
    sector_icon = models.TextField()
    sector_cat_id = models.ManyToManyField(SectorCat)


class EmissionsName(models.Model):
    emissions_name = models.TextField(default="")
    model_id = models.ManyToManyField(ModelsInfo,
                                      through='EmissionsStates')
    ordering = models.IntegerField(default=0)


class EmissionsIcon(models.Model):
    emissions_icon_name = models.TextField()
    emission_name = models.ManyToManyField(EmissionsName)


class EmissionsStates(models.Model):
    emissions_name_id = models.ForeignKey(EmissionsName,
                               on_delete=models.CASCADE)
    model_id = models.ForeignKey(ModelsInfo,
                              on_delete=models.CASCADE)
    state = models.TextField()


class SocioeconsCat(models.Model):
    socioecons_cat = models.TextField(default="")
    ordering = models.IntegerField(default=0)


class SocioeconsIcon(models.Model):
    socioecons_icons = models.TextField()
    # socioecons_cat_id = models.ManyToManyField(SocioeconsCat)
    socioecons_cat_id = models.ManyToManyField(SocioeconsCat)


class SocioeconsName(models.Model):
    socioecons_name = models.TextField()
    socioecons_cat_id = models.ManyToManyField(SocioeconsCat)
    model_id = models.ManyToManyField(ModelsInfo,
                                      through='SocioeconsStates')
    ordering = models.IntegerField(default=0)


class SocioeconsStates(models.Model):
    socioecons_name_id = models.ForeignKey(SocioeconsName,
                               on_delete=models.CASCADE)
    model_id = models.ForeignKey(ModelsInfo,
                              on_delete=models.CASCADE)
    state = models.TextField()


class PoliciesCat(models.Model):
    policies_cat = models.TextField()
    ordering = models.IntegerField(default=0)


class PoliciesIcon(models.Model):
    policies_icon = models.TextField()
    policies_cat = models.ManyToManyField(PoliciesCat)


class PoliciesName(models.Model):
    policies_name = models.TextField()
    policies_cat_id = models.ManyToManyField(PoliciesCat)
    model_id = models.ManyToManyField(ModelsInfo,
                                      through='PoliciesStates')
    ordering = models.IntegerField(default=0)


class PoliciesStates(models.Model):
    policies_name_id = models.ForeignKey(PoliciesName,
                               on_delete=models.CASCADE)
    model_id = models.ForeignKey(ModelsInfo,
                              on_delete=models.CASCADE)
    state = models.TextField()
