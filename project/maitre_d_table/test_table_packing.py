from django.test import TransactionTestCase

from reserve_table import pack_table, UnableToPackTablesError


class MockReservation(object):

    def __init__(self, people):
        self.people = people


def create_reservation_list(party_size_list):
    return [MockReservation(p) for p in party_size_list]


class TestPackTable(TransactionTestCase):

    def test_packs_single_reservation_to_single_tabled_restaurant(self):
        reservation_list = create_reservation_list([2])
        table_list = [2]

        table_seating = pack_table(reservation_list, table_list)

        self.assertEqual(
            table_seating,
            [(reservation_list[0], (2, )), ]
        )

    def test_packs_two_tables_of_differing_sizes(self):
        reservation_list = create_reservation_list([2, 4])
        table_list = [2, 4]

        table_seating = pack_table(reservation_list, table_list)

        self.assertEqual(
            table_seating,
            [
                (reservation_list[0], (2, )),
                (reservation_list[1], (4, )),
            ]
        )

    def test_packs_to_exact_fit_on_single_table(self):
        reservation_list = create_reservation_list([2, 4])
        table_list = [3, 2, 5, 4]

        table_seating = pack_table(reservation_list, table_list)

        self.assertEqual(
            table_seating,
            [
                (reservation_list[0], (2, )),
                (reservation_list[1], (4, )),
            ]
        )

    def test_raises_error_if_insufficient_tables_to_seat_resevations(self):
        reservation_list = create_reservation_list([2, 2, 2])
        table_list = [2, 2]

        with self.assertRaises(UnableToPackTablesError):
            pack_table(reservation_list, table_list)

    def test_packs_to_exact_fit_on_multiple_tables(self):
        reservation_list = create_reservation_list([10, 6])
        table_list = [2, 4, 4, 6]

        table_seating = pack_table(reservation_list, table_list)

        self.assertEqual(
            table_seating,
            [
                (reservation_list[1], (6, )),
                (reservation_list[0], (2, 4, 4))
            ]
        )
