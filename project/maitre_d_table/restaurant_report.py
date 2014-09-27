from restaurant.models import Restaurant


def restaurant_report(restaurant_name, date):
    restaurant = Restaurant.objects.get(name=restaurant_name)

    reservations = restaurant.reservations_on_date(date)
    covers = sum([res.people for res in reservations])
    return dict(covers=covers)
