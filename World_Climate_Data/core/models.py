from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField

class Station(models.Model):
    mins = models.EmbeddedModelField('Months')
    maxes = models.EmbeddedModelField('Months')
    elevation = models.DecimalField()
    coordinates = models.ListField(models.FloatField())
    StationName = models.CharField()
    WMOStationNumber = models.IntegerField()

class Months(models.Model):
    Jan = models.FloatField()
    Feb = models.FloatField()
    Mar = models.FloatField()
    Apr = models.FloatField()
    May = models.FloatField()
    Jun = models.FloatField()
    Jul = models.FloatField()
    Aug = models.FloatField()
    Sep = models.FloatField()
    Oct = models.FloatField()
    Nov = models.FloatField()
    Dec = models.FloatField()
