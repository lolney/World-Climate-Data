from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField
from django_mongodb_engine.contrib import MongoDBManager

class Station(models.Model):
    mins = EmbeddedModelField('Months')
    maxes = EmbeddedModelField('Months')
    elevation = models.FloatField()
    coordinates = ListField(models.FloatField())
    StationName = models.CharField(max_length=100)
    WMOStationNumber = models.IntegerField()

    objects = MongoDBManager()

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
    
