from django.db import models

# Create your models here.

class Weather(models.Model):
    temperature = models.IntegerField()
    humid = models.IntegerField()
    dust = models.IntegerField()
    superdust = models.IntegerField()
    tvoc = models.FloatField()

    def __str__(self):
        return self.temperature
