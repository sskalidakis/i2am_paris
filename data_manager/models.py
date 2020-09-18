from django.db import models


class Query(models.Model):
    query_name = models.CharField(null=False, default="", max_length=50)
    parameters = models.TextField(null=True, default="{}", max_length=1000)
    dataset = models.CharField(null=False, default="", max_length=50)