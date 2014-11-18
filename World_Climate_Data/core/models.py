from django.db import models
from djangotoolbox.fields import ListField, DictField

class Station(models.Model):
    mins = DictField(models.FloatField())
    maxes = DictField(models.FloatField())
    elevation = models.DecimalField(decimal_places=5, max_digits=10)
    coordinates = ListField(models.FloatField())
    StationName = models.CharField(max_length=100)
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
