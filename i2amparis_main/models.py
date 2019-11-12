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


    def __str__(self):
        return self.model_name


class Sectors(models.Model):
    """
    Tab Sectoral Granularity

    """
    category = models.TextField()
    subcategory = models.TextField(default="")
    name = models.TextField()
    icon = models.TextField(default="")
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.name


class Emissions(models.Model):
    """
    Tab Emission Granularity

    """
    categories = models.TextField()  # TODO change the name to category
    name = models.TextField()
    state = models.TextField()
    icon = models.TextField(default="")
    model_name = models.ManyToManyField(ModelsInfo)
    title = models.TextField(default="")

    def __str__(self):
        return self.name


class Socioecons(models.Model):
    """
    Tab Socioecons Granularity

    """
    category = models.TextField()
    subcategory = models.TextField(default="")
    name = models.TextField()
    state = models.TextField()
    icon = models.TextField(default="")
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.name


class Policies(models.Model):
    """
    Tab Policy Granularity

    """
    category = models.TextField()
    name = models.TextField()
    state = models.TextField()
    icon = models.TextField(default="")
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.name


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


class Mitigations(models.Model):
    """
    Tab Mitigation-Adaptation measures(1)

    """
    category = models.TextField()
    subcategory = models.TextField(default="")
    name = models.TextField()
    icon = models.TextField(default="")
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.name


class Adaptation(models.Model):
    """
    Tab Mitigation-Adaptation measures(2)

    """
    category = models.TextField()
    name = models.TextField()
    icon = models.TextField(default="")
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.name


class Sdgs(models.Model):
    """
    Tab SDG Granularity

    """
    name = models.TextField()
    title = models.TextField(default="")
    description = models.TextField()
    icon = models.TextField(default="")
    model_name = models.ManyToManyField(ModelsInfo)

    def __str__(self):
        return self.name
