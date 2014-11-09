from django.db import models
from django.contrib.auth.models import User as DjangoUser

class Poll(models.Model):
    question = models.CharField(unique=True, max_length=200)
    creator = models.ForeignKey('User')
    up_votes = models.IntegerField()
    down_votes = models.IntegerField()

class User(models.Model):
    user = models.ForeignKey(DjangoUser, blank=True, null=True)
    facebook_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=200)

