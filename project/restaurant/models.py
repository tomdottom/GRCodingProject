from django.db import models

from datetime import timedelta

# isoweekday
WEEKDAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
]


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=False)
    _tables = models.TextField(default='2,2,4,4')

    def __unicode__(self):
        return "%s" % (self.name)

    @property
    def tables(self):
        return [int(x) for x in self._tables.split(',')]

    @tables.setter
    def tables(self, value):
        tables = [i for i in value if type(i) == int]
        tables = reduce(lambda x, y: '%s,%s' % (x, y), tables)
        self._tables = tables

    def is_open(self, dt):
        ot = self.opening_times.filter(weekday=dt.isoweekday()).first()
        if ot is None:
            return False
        return ot.fromHour < dt.time() < ot.toHour

    def is_closed(self, dt):
        return not self.is_open(dt)

    def reservations_ongoing(self, datetime):
        reservation_duration = timedelta(hours=1.5)

        return list(
            self.reservations.filter(
                datetime__gte=(datetime - reservation_duration),
                datetime__lte=(datetime + reservation_duration)
            ).order_by('people')
        )


class OpeningTime(models.Model):

    restaurant = models.ForeignKey(Restaurant, related_name='opening_times')
    weekday = models.IntegerField(choices=WEEKDAYS)
    fromHour = models.TimeField()
    toHour = models.TimeField()

    class Meta:
        verbose_name_plural = "stories"

    def __unicode__(self):
        return "%s %s (%s - %s)" % (
            self.restaurant, self.weekday, self.fromHour, self.toHour)
