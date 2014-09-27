from django.db import models

from restaurant.models import Restaurant


class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='reservations')
    datetime = models.DateTimeField()
    people = models.IntegerField()
