from restaurant.models import Restaurant
from reservation.models import Reservation

from operator import attrgetter


class RestaurantClosedError(Exception):
    pass


class NoSuchRestaurantError(Exception):
    pass


class NoTableLargeEnoughError(Exception):
    pass


class ReservationNotPossibleError(Exception):
    pass


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


def reserve_table(restaurant_name, time, people):
    try:
        restaurant = Restaurant.objects.get(name=restaurant_name)
    except Restaurant.DoesNotExist:
        raise NoSuchRestaurantError

    if restaurant.is_closed(time):
        raise RestaurantClosedError

    if max(restaurant.tables) < people:
        raise NoTableLargeEnoughError

    current_reservations = restaurant.reservations_ongoing(time)

    new_res = Reservation(
        restaurant=restaurant,
        datetime=time,
        people=people
    )

    if table_available(current_reservations + [new_res], restaurant.tables):
        new_res.save()
        return new_res.id

    raise ReservationNotPossibleError
