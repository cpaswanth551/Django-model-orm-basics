from django.shortcuts import render

from restaurant.models import Rating, Restaurant, Staff, StaffRestaurant

# Create your views here.


def index_prefect_related(request):
    rest_ = Restaurant.objects.all()  # will take 15 queries
    rest__ = Restaurant.objects.prefetch_related("ratings")  # takes 2 queries.
    rest = Restaurant.objects.filter(name__istartswith="P").prefetch_related("ratings")
    context = {"restaurant": rest}
    return render(request, "index.html", context)


def index_select_related(request):
    rating = Rating.objects.all()  # taking 31 queries
    rating_sr = Rating.objects.only("rating", "restaurant__name").select_related(
        "restaurant"
    )  # only took 1 query
    context = {"ratings": rating_sr}
    return render(request, "index.html", context)


def index_m2m(request):
    staff, created = Staff.objects.get_or_create(name="Aswanth CP")
    print(staff.restaurant.all())
    staff.restaurant.add(Restaurant.objects.first())  # adding new m2m relations
    staff.restaurant.set(Restaurant.objects.all()[0:10])  # slicing 0 to <10
    print(staff.restaurant.all())
    staff.restaurant.remove(Restaurant.objects.first())  # removing new m2m relations
    staff.restaurant.set(Restaurant.objects.all())  # sets all restaurant to the staff
    staff.restaurant.clear()  # remove all relations
    italian = staff.restaurant.filter(
        restaurant_type=Restaurant.TypeChoices.ITALIAN
    )  # filtering
    print(staff.restaurant.count())  # counts of all relations

    rest = Restaurant.objects.first()  # reverse accessing
    staff = rest.staff_set.all()
    return render(request, "index.html")


def index_m2m_through(request):
    context = {}
    staff = Staff.objects.first()
    rest = Restaurant.objects.first()
    rest2 = Restaurant.objects.last()
    staff_rest = StaffRestaurant.objects.create(
        staff=staff, restaurant=rest, salary=24_000
    )  # adding element to m2m through staffRestaurant model
    staff.restaurants.add(
        rest, through_defaults={"salary": 28_000}
    )  # alternate way to add staff restaurant

    return render(request, "index.html", context)


def index_m2m_query(request):
    context = {}
    jobs = (
        StaffRestaurant.objects.all()
    )  # here we are having total of 23 queries when try to use this query technique

    for job in jobs:
        print(job.restaurant)
        print(job.staff)

    # same thing will optimized using prefetch query
    jobs = StaffRestaurant.objects.prefetch_related("restaurant", "staff")

    for job in jobs:
        print(job.restaurant)
        print(job.staff)

    return render(request, "index.html", context)
