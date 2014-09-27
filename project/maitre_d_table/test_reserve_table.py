import datetime

from django.test import TransactionTestCase

from reserve_table import (
    reserve_table,
    RestaurantClosedError, NoSuchRestaurantError
)


class TestReserveTable(TransactionTestCase):

    fixtures = ['test_restaurants.json']

    def test_returns_reservation_number(self):
        time = datetime.datetime(2014, 3, 4, 13, 30)

        reservation = reserve_table('Small', time, 3)

        self.assertIsInstance(reservation, int)

    def test_reservations_for_non_existant_restaurant_raise_error(self):
        time = datetime.datetime(2014, 3, 4, 02, 30)

        with self.assertRaises(NoSuchRestaurantError):
            reserve_table('No Name', time, 3)

    def test_reservations_when_restaurant_closed_raise_error(self):
        time = datetime.datetime(2014, 3, 4, 02, 30)

        with self.assertRaises(RestaurantClosedError):
            reserve_table('Small', time, 3)
