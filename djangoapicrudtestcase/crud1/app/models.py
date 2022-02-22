from django.db import models


# Create your models here.
class Information(models.Model):
    name = models.CharField(max_length=40)
    idCard = models.IntegerField()
    roll = models.IntegerField()
