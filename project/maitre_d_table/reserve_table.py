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

    for allow_table_error in range(2):
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

    def tables_gen(table_list, num_of_tables):
        table_indexes = table_indexes_gen(len(table_list), num_of_tables)
        for indexes in table_indexes:
            yield [table_list[i] for i in indexes]

    for tables in tables_gen(table_list, min(max_tables, len(table_list))):
        if allow_table_error:
            if reservation.people <= sum(tables):
                return tuple(tables)
        else:
            if reservation.people == sum(tables):
                return tuple(tables)

    return None


def table_available(reservation_list, tables):
    sorted_tables = sorted(tables)
    sorted_res = sorted(reservation_list, key=attrgetter('people'))

    try:
        for res in sorted_res:
            while res.people > sorted_tables[0]:
                sorted_tables.pop(0)
            sorted_tables.pop(0)
    except IndexError:
        return False

    return True


def reserve_table(restaurant_name, dt, people):

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

    if max(restaurant.tables) < people:
        raise ReservationNotPossibleError(
            "No table large enough to accomodate %s poeple" % (people, )
        )

    current_reservations = restaurant.reservations_ongoing(dt)

    new_res = Reservation(
        restaurant=restaurant,
        datetime=dt,
        people=people
    )

    if restaurant.is_closed(new_res.endtime):
        raise ReservationNotPossibleError

    if table_available(current_reservations + [new_res], restaurant.tables):
        new_res.save()
        return new_res.id
    else:
        raise ReservationNotPossibleError(
            "No table large enough is available to accomodate %s people" % (
                people, )
        )

    raise ReservationNotPossibleError
