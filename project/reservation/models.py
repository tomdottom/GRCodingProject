from datetime import timedelta
from django.db import models

from restaurant.models import Restaurant


class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='reservations')
    datetime = models.DateTimeField()
    people = models.IntegerField()
    _length = models.IntegerField(default=5400) #5400 seconds = 1.5 hours

    @property
    def endtime(self):
        return self.datetime + timedelta(seconds=self._length)
