from operator import attrgetter
import pytz

from restaurant.models import Restaurant
from reservation.models import Reservation


class RestaurantClosedError(Exception):
    pass


class NoSuchRestaurantError(Exception):
    pass


class ReservationNotPossibleError(Exception):
    pass


class UnableToPackTablesError(Exception):
    pass


def pack_tables(reservation_list, table_list):
    sorted_res = sorted(reservation_list, key=attrgetter('people'))
    sorted_tables = sorted(table_list)

    packed_tables = []

    # increasing spare seats
    for allow_table_error in range(2):
        # increasing table combinations
        for max_tables in range(1, len(sorted_tables)+1):

            for res in sorted_res:
                tables = match_tables_to_reservation(
                    res, sorted_tables, max_tables, allow_table_error)

                if tables is not None:
                    for t in tables:
                        sorted_tables.remove(t)
                    packed_tables.append((res, tables))

            for table in packed_tables:
                try:
                    sorted_res.remove(table[0])
                except ValueError:
                    pass

    if len(sorted_res) == 0:
        return packed_tables

    raise UnableToPackTablesError()


def match_tables_to_reservation(
        reservation, table_list, max_tables, allow_table_error=False):

    # generate a sequence of integers to use as index, ie
    # length_of_list = 5, num_of_tables = 3
    # [0, 1, 2]
    # [0, 1, 3]
    # [0, 1, 4]
    # [0, 2, 3]
    # [0, 2, 4]
    # ....
    # [2, 3, 4]
    def table_indexes_gen(length_of_list, num_of_tables):
        if length_of_list > 0 and num_of_tables > 0:
            table_indexes = range(num_of_tables)
            while True:
                yield table_indexes
                if table_indexes[0] == (length_of_list - num_of_tables):
                    break
                if table_indexes[-1] == (length_of_list - 1):
                    for i in range(num_of_tables-1, -1, -1):
                        if table_indexes[i-1] < (table_indexes[i]-1):
                            table_indexes[i-1] += 1
                            for j in range(i, num_of_tables, 1):
                                table_indexes[j] = table_indexes[j-1] + 1
                            break
                else:
                    table_indexes[-1] += 1

    def table_combo_gen(table_list, num_of_tables):
        table_indexes = table_indexes_gen(len(table_list), num_of_tables)
        for indexes in table_indexes:
            yield [table_list[i] for i in indexes]

    for tables in table_combo_gen(
            table_list, min(max_tables, len(table_list))):

        if allow_table_error:
            if reservation.people <= sum(tables):
                return tuple(tables)
        else:
            if reservation.people == sum(tables):
                return tuple(tables)

    return None


def reserve_table(restaurant_name, dt, people, reservation_length_hrs=None):

    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    try:
        restaurant = Restaurant.objects.get(name=restaurant_name)
    except Restaurant.DoesNotExist:
        raise NoSuchRestaurantError(
            "Could not retrieve restaurant named %s" % (restaurant_name, )
        )

    if restaurant.is_closed(dt):
        raise RestaurantClosedError

    current_reservations = restaurant.reservations_ongoing(dt)

    if reservation_length_hrs is None:
        # 5400 seconds = 1.5hrs
        _length = 5400
    else:
        _length = reservation_length_hrs * 3600

    new_res = Reservation(
        restaurant=restaurant,
        datetime=dt,
        people=people,
        _length=_length
    )

    if restaurant.is_closed(new_res.endtime):
        raise ReservationNotPossibleError

    try:
        pack_tables(current_reservations + [new_res], restaurant.tables)
        new_res.save()
        return new_res.id
    except UnableToPackTablesError:
        raise ReservationNotPossibleError(
            "Not enough tables available to accomodate %s people" % (
                people, )
        )

    raise ReservationNotPossibleError
