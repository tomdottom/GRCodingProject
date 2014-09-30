import datetime
import pytz

from django.test import TransactionTestCase

from reserve_table import (
    reserve_table,
    RestaurantClosedError, NoSuchRestaurantError, ReservationNotPossibleError
)
from restaurant.models import Restaurant
from reservation.models import Reservation


class TestReserveTable(TransactionTestCase):

    fixtures = ['test_restaurants.json']

    def test_raises_error_for_non_existant_restaurant(self):
        time = datetime.datetime(2014, 3, 4, 02, 30)

        with self.assertRaises(NoSuchRestaurantError) as e:
            reserve_table('No Name', time, 3)

        self.assertEqual(
            e.exception.args[0],
            "Could not retrieve restaurant named No Name"
        )

    def test_raises_error_if_reservation_begins_when_restaurant_closed(self):
        time = datetime.datetime(2014, 3, 4, 02, 30)

        with self.assertRaises(RestaurantClosedError):
            reserve_table('Small', time, 3)

    def test_raises_error_when_restaurant_does_not_have_opening_hours(self):
        time = datetime.datetime(2014, 3, 3, 12, 30)

        with self.assertRaises(RestaurantClosedError):
            reserve_table('Small', time, 3)

    def test_raises_error_if_reservation_will_run_past_closing_time(self):
        time = datetime.datetime(2014, 3, 4, 21, 30)

        with self.assertRaises(ReservationNotPossibleError):
            reserve_table('Small', time, 3)

    def test_raises_error_if_no_table_large_enough_to_accomodate_party(self):
        time = datetime.datetime(2014, 3, 4, 13, 30)

        with self.assertRaises(ReservationNotPossibleError) as e:
            reserve_table('Small', time, 13)

        self.assertEqual(
            e.exception.args[0],
            "Not enough tables available to accomodate 13 people"
        )

    def test_creates_new_reservation(self):
        time = datetime.datetime(2014, 3, 4, 13, 30)

        reserve_table('Small', time, 2)

        r = Restaurant.objects.get(name='Small')
        self.assertEqual(
            r.reservations.count(),
            1
        )

    def test_returns_reservation_id(self):
        time = datetime.datetime(2014, 3, 4, 13, 30)

        reservation = reserve_table('Small', time, 3)

        self.assertIsInstance(reservation, int)

    def test_raises_error_if_all_tables_booked(self):
        time = datetime.datetime(2014, 3, 4, 13, 30)
        reserve_table('Small', time, 2)
        reserve_table('Small', time, 2)
        reserve_table('Small', time, 4)
        reserve_table('Small', time, 4)

        with self.assertRaises(ReservationNotPossibleError) as e:
            reserve_table('Small', time, 2)

        self.assertEqual(
            e.exception.args[0],
            "Not enough tables available to accomodate 2 people"
        )

    def test_saves_as_utc_if_naive_datetime_used(self):
        naive_dt = datetime.datetime(2014, 3, 4, 13, 30)

        reserve_table('Small', naive_dt, 2)

        restaurant = Restaurant.objects.get(name='Small')
        reservation = restaurant.reservations.first()

        reservation.datetime.tzinfo == pytz.utc

    def test_can_book_accross_multiple_tables(self):
        time = datetime.datetime(2014, 3, 4, 13, 30)

        reserve_table('Odd', time, 7)
        reservation = reserve_table('Odd', time, 8)

        self.assertIsInstance(reservation, int)

    def test_can_reserve_a_table_for_custom_length_of_time(self):
        time = datetime.datetime(2014, 3, 4, 13, 30)

        reservation_id = reserve_table('Odd', time, 8, 5)
        reservation = Reservation.objects.get(id=reservation_id)

        self.assertEqual(
            reservation.endtime,
            datetime.datetime(2014, 3, 4, 18, 30, tzinfo=pytz.utc)

        )
