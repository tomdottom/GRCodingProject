import datetime
from django.test import TransactionTestCase

from reserve_table import reserve_table

from restaurant_report import restaurant_report


class TestRestaurantReport(TransactionTestCase):

    fixtures = ['test_restaurants.json']

    # error if restaurant doesn't exist

    def test_returns_daily_cover_count(self):
        reserve_table('Small', datetime.datetime(2014, 3, 4, 12, 30), 2)

        data = restaurant_report('Small', datetime.date(2014, 3, 4))

        self.assertEqual(data['covers'], 2)
