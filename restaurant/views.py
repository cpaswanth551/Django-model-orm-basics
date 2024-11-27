from datetime import timezone, datetime, timedelta
from django.shortcuts import render
from django.db.models.functions import Lower, Length, Concat
from django.db.models import Count, Avg, Max, Min, Sum, CharField, Value

from .models import Restaurant, Rating, Sale, Staff, StaffRestaurant


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


def index_values(request):
    context = {}
    restaurant = Restaurant.objects.values("name")  # here the values will a dict output
    restaurant2 = Restaurant.objects.values(name_lower=Lower("name"))[:5]
    rst3 = Restaurant.objects.values("name", "date_opened")

    IT = Restaurant.TypeChoices.ITALIAN
    rating = Rating.objects.filter(restaurant__restaurant_type=IT).values(
        "rating", "restaurant__name"
    )  # here we can access the related restaurant element of rating  model using values.
    print(rating)
    return render(request, "index.html", context)


def index_values_list(request):
    context = {}
    restaurant = Restaurant.objects.values_list(
        "name"
    )  # her the values are given in tuples.

    restaurant = Restaurant.objects.values_list(
        "name", flat=True
    )  # here the values are given in list

    print(restaurant)
    return render(request, "index.html", context)


def index_aggregate(request):
    context = {}
    ret_count = Restaurant.objects.count()
    print(ret_count)

    rest = Restaurant.objects.aggregate(total=Count("id"))
    print(rest)

    rest_avg = Rating.objects.aggregate(avg=Avg("rating"))
    print(rest_avg)

    rest_avg1 = Rating.objects.filter(restaurant__name__startswith="p").aggregate(
        avg=Avg("rating")
    )
    print(rest_avg1)

    sale_icome_max = Sale.objects.aggregate(max=Max("income"))
    sale_icome_min = Sale.objects.aggregate(min=Min("income"))
    sale_icome = Sale.objects.aggregate(
        min=Min("income"), max=Max("icome"), avg=Avg("income"), sum=Sum("income")
    )
    print(sale_icome_max, sale_icome_min)

    one_month_ago = datetime.now() - timedelta(days=31)
    sales = Sale.objects.filter(datetime__gte=one_month_ago)
    sale_icome = sales.aggregate(
        min=Min("income"), max=Max("income"), avg=Avg("income"), sum=Sum("income")
    )
    print(sale_icome)

    return render(request, "index.html", context)


def index_annotate(request):
    context = {}
    restaurant = Restaurant.objects.annotate(name_len=Length("name"))
    restaurant1 = Restaurant.objects.annotate(name_len=Length("name")).filter(
        name_len__gte=10
    )
    print(restaurant1.values("name", "name_len"))

    return render(request, "index.html", context)


def index_annotate_ex(request):
    context = {}
    concatenation = Concat(
        "name",
        Value(" [Rating: "),
        Avg("ratings__rating"),
        Value("]"),
        output_field=CharField(),
    )
    rest = Restaurant.objects.annotate(
        message=concatenation
    )  #  addes {"message" : "Pizzeria 2 [Rating: 3.0]"}
    for r in rest:
        print(r.message)

    rest_total_sales = Restaurant.objects.annotate(
        total_sales=Sum("sales__income")
    ).values("name", "total_sales")

    rest_count = Restaurant.objects.annotate(
        num_rating=Count("ratings__rating")
    ).values("name", "num_rating")

    rest_count_with_avg = Restaurant.objects.annotate(
        num_rating=Count("ratings__rating"), avg_rating=Avg("ratings__rating")
    ).values("name", "num_rating", "avg_rating")

    rest_count_with_groupby_rest_type = Restaurant.objects.values(
        "restaurant_type"
    ).annotate(
        num_rating=Count("ratings__rating")
    )  # This will give distinct restaurant_type rating count

    print([r["total_sales"] for r in rest_count])
    rest_sales_total = Restaurant.objects.annotate(
        total_sales=Sum("sales__income")
    ).order_by("total_sales")

    for r in rest_sales_total:
        print(r.total_sales)

    rest_sales_total = Restaurant.objects.annotate(
        total_sales=Sum("sales__income")
    ).order_by("total_sales")

    print(rest_sales_total.aggregate(avg_sales=Avg("total_sales")))

    return render(request, "index.html", context)


def index(request):
    context = {}

    return render(request, "index.html", context)
