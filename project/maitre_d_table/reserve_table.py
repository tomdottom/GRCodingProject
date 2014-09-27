from restaurant.models import Restaurant


class RestaurantClosedError(Exception):
    pass


class NoSuchRestaurantError(Exception):
    pass


def reserve_table(restaurant_name, time, people):
    try:
        restaurant = Restaurant.objects.get(name=restaurant_name)
    except Restaurant.DoesNotExist:
        raise NoSuchRestaurantError

    if restaurant.is_closed(time):
        raise RestaurantClosedError

    return 1
