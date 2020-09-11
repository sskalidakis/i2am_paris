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
    coverage_title = models.TextField(default="")
    harmonisation = models.BooleanField(default=False)

    def __str__(self):
        return self.model_name


# Data Used only for the harmonisation Heatmap Application
class Harmonisation_Variables(models.Model):
    """Variables for harmonisation table"""
    var_name = models.CharField(null=False, default="", max_length=50)
    var_title = models.CharField(null=False, default="", max_length=50)
    var_category = models.CharField(null=False, default="", max_length=50)
    var_definition = models.TextField(null=False, default="")
    model_relation = models.ManyToManyField(ModelsInfo, through='HarmData')
    order = models.IntegerField(null=False, default=1)


class HarmData(models.Model):
    model = models.ForeignKey(ModelsInfo, on_delete=models.CASCADE)
    variable = models.ForeignKey(Harmonisation_Variables, on_delete=models.CASCADE)
    io_status = models.CharField(null=False, default="", max_length=50)
    var_unit = models.CharField(null=False, default="", max_length=20)
    var_source_info = models.TextField(null=False, default="")
    var_timespan = models.TextField(null=False, default="")


# Data Variable Tables
class DataVariablesModels(models.Model):
    """
    Models for data model
    """
    name = models.TextField()
    title = models.TextField(default="")
    type = models.TextField()
    time_horizon = models.IntegerField()
    time_steps_in_solution = models.IntegerField(default=0)
    ordering = models.IntegerField(default=0)
    coverage = models.TextField(default="")
    coverage_title = models.TextField(default="")


class DataVariablesHarmonisation(models.Model):
    """HarmVariables for data model"""
    name = models.CharField(null=False, default="", max_length=50)
    title = models.CharField(null=False, default="", max_length=50)
    category = models.CharField(null=False, default="", max_length=50)
    order = models.IntegerField(null=False, default=1)


#Datasets
class DatasetVariableHarmonisation(models.Model):
    harmonisation_model = models.ForeignKey(DataVariablesModels, on_delete=models.CASCADE)
    harmonisation_variable = models.ForeignKey(DataVariablesHarmonisation, on_delete=models.CASCADE)
    harmonisation_io_status = models.CharField(null=False, default="", max_length=50)

# Guide Datasets

class DatasetVariableHarmonisationGuides(models.Model):
    guide_from = models.CharField(null=False, default="", max_length=50)
    guide_to = models.CharField(null=False, default="", max_length=50)
    value = models.CharField(null=False, default="", max_length=50)


class DatasetModelGeoGuides(models.Model):
    guide_from = models.CharField(null=False, default="", max_length=50)
    guide_to = models.CharField(null=False, default="", max_length=50)
    value = models.CharField(null=False, default="", max_length=50)

class DatasetModelTypeGuides(models.Model):
    guide_from = models.CharField(null=False, default="", max_length=50)
    guide_to = models.CharField(null=False, default="", max_length=50)
    value = models.CharField(null=False, default="", max_length=50)


class DatasetModelTimestepGuides(models.Model):
    guide_from = models.CharField(null=False, default="", max_length=50)
    guide_to = models.CharField(null=False, default="", max_length=50)
    value = models.CharField(null=False, default="", max_length=50)


# Data Model
class Dataset(models.Model):
    """dataset name is the name of table containing the data of the specific dataset"""
    dataset_name = models.CharField(null=False, default="", max_length=50)
    dataset_title = models.CharField(null=False, default="", max_length=50)
    dataset_description = models.TextField(null=False, default="")
    dataset_provider = models.CharField(null=False, default="", max_length=50)
    dataset_date_creation = models.DateTimeField(auto_now_add=True)
    dataset_date_update = models.DateTimeField(auto_now=True)
    dataset_django_model = models.CharField(null=False, default="", max_length=50)


class Variable(models.Model):
    var_name = models.CharField(null=False, default="", max_length=50)
    var_title = models.CharField(null=False, default="", max_length=50)
    var_category = models.CharField(null=False, default="", max_length=50)
    var_definition = models.TextField(null=False, default="")
    var_unit = models.CharField(null=False, default="", max_length=50)
    dataset_relation = models.ForeignKey(Dataset, null=False, on_delete=models.CASCADE)
    variable_table_name = models.CharField(null=True, max_length=50)


# Dynamic Documentation Models

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


class SdgsCat(models.Model):
    sdgs_cat = models.TextField()
    sdgs_title = models.TextField()
    ordering = models.IntegerField(default=0)
    model_id = models.ManyToManyField(ModelsInfo,
                                      through='SdgsName')


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


# Feedback Form Models
class Feedback(models.Model):
    username = models.CharField(max_length=120)
    email = models.CharField(default='', max_length=120)
    subject = models.CharField(default='', max_length=120)
    message = models.TextField(default='')

    def __str__(self):
        return self.username
