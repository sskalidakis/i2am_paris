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
    partener = models.TextField()
    type_of_model = models.TextField()
    time_horizon = models.IntegerField()
    time_steps_in_solution = models.IntegerField()
    model_descr = models.TextField()

    def __str__(self):
        return self.model_name


class Sectors(models.Model):
    """
    Tab Sectoral Granularity

    """
    category = models.TextField()
    subcategory = models.TextField(default="")
    sector = models.TextField()
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.sector


class Emissions(models.Model):
    """
    Tab Emission Granularity

    """
    categories = models.TextField()
    emission = models.TextField()
    state = models.TextField()
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.emission


class Socioecons(models.Model):
    """
    Tab Socioecons Granularity

    """
    category = models.TextField()
    subcategory = models.TextField(default="")
    socioecon = models.TextField()
    state = models.TextField()
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.socioecon


class Policies(models.Model):
    """
    Tab Policy Granularity

    """
    category = models.TextField()
    policy = models.TextField()
    state = models.TextField()
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.policy


class Regions(models.Model):
    """
    Tab Regional Granularity(1)

    """
    region = models.TextField()
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.region


class Countries(models.Model):
    """
    Tab Regional Granularity(2)

    """
    country_name = models.TextField()
    country_code = models.CharField(max_length=3)
    region = models.ManyToManyField(Regions)
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.country_name


class Mitigations(models.Model):
    """
    Tab Mitigation-Adaptation measures(1)

    """
    category = models.TextField()
    subcategory = models.TextField(default="")
    measure = models.TextField()
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.measure


class Adaptation(models.Model):
    """
    Tab Mitigation-Adaptation measures(2)

    """
    category = models.TextField()
    measure = models.TextField()
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.measure


class Sdgs(models.Model):
    """
    Tab SDG Granularity

    """
    sdg_name = models.TextField()
    description = models.TextField()
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.sdg_name
