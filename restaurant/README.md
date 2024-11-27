# Django QuerySet Optimization and Advanced Querying Techniques

## Overview
This README covers advanced Django QuerySet techniques for efficient database querying, focusing on performance optimization, relationship handling, and data retrieval strategies.

## 1. Prefetch Related vs Select Related

### `index_prefect_related()`
```python
def index_prefect_related(request):
    rest_ = Restaurant.objects.all()  # will take 15 queries
    rest__ = Restaurant.objects.prefetch_related("ratings")  # takes 2 queries
    rest = Restaurant.objects.filter(name__istartswith="P").prefetch_related("ratings")
```

#### Key Concepts:
- **Prefetch Related**: Optimizes queries for Many-to-Many and reverse Foreign Key relationships
- Reduces number of database queries from 15 to 2
- Useful for efficiently loading related objects

#### Example Use Case:
```python
# Without prefetch_related (inefficient)
restaurants = Restaurant.objects.all()
for restaurant in restaurants:
    print(restaurant.ratings.count())  # Generates multiple queries

# With prefetch_related (efficient)
restaurants = Restaurant.objects.prefetch_related("ratings")
for restaurant in restaurants:
    print(restaurant.ratings.count())  # Minimizes database hits
```

## 2. Select Related 

### `index_select_related()`
```python
def index_select_related(request):
    rating = Rating.objects.all()  # taking 31 queries
    rating_sr = Rating.objects.only("rating", "restaurant__name").select_related("restaurant")  # only took 1 query
```

#### Key Concepts:
- **Select Related**: Optimizes Foreign Key and One-to-One relationships
- Reduces queries from 31 to 1
- Use `.only()` to select specific fields, further reducing data transfer

#### Example Use Case:
```python
# Inefficient approach
ratings = Rating.objects.all()
for rating in ratings:
    print(rating.restaurant.name)  # Generates multiple queries

# Efficient approach
ratings = Rating.objects.select_related('restaurant')
for rating in ratings:
    print(rating.restaurant.name)  # Single efficient query
```

## 3. Many-to-Many Relationships

### `index_m2m()`
```python
def index_m2m(request):
    staff, created = Staff.objects.get_or_create(name="Aswanth CP")
    
    # M2M Relationship Management Methods
    staff.restaurant.add(Restaurant.objects.first())  # Add single restaurant
    staff.restaurant.set(Restaurant.objects.all()[0:10])  # Set multiple restaurants
    staff.restaurant.remove(Restaurant.objects.first())  # Remove specific restaurant
    staff.restaurant.clear()  # Remove all relations
    
    # Filtering M2M Relationships
    italian = staff.restaurant.filter(restaurant_type=Restaurant.TypeChoices.ITALIAN)
    print(staff.restaurant.count())  # Count of relationships
```

#### Key Concepts:
- Multiple methods to manage Many-to-Many relationships
- Easy filtering and manipulation of related objects
- Reverse relationship access with `staff_set`

## 4. Many-to-Many Through Model

### `index_m2m_through()`
```python
def index_m2m_through(request):
    staff = Staff.objects.first()
    rest = Restaurant.objects.first()
    
    # Creating through model instance
    staff_rest = StaffRestaurant.objects.create(
        staff=staff, restaurant=rest, salary=24_000
    )
    
    # Alternate way to add with additional data
    staff.restaurants.add(rest, through_defaults={"salary": 28_000})
```

#### Key Concepts:
- Use of intermediate model to store additional data
- Flexible relationship management
- Allows storing extra information about the relationship

## 5. Values and Values List

### `index_values()`
```python
def index_values(request):
    restaurant = Restaurant.objects.values("name")  # Dict output
    restaurant2 = Restaurant.objects.values(name_lower=Lower("name"))[:5]
    rating = Rating.objects.filter(restaurant__restaurant_type=IT).values(
        "rating", "restaurant__name"
    )
```

#### Key Concepts:
- `values()`: Returns dictionaries instead of model instances
- Can annotate and transform fields
- Useful for lightweight data retrieval

### `index_values_list()`
```python
def index_values_list(request):
    restaurant = Restaurant.objects.values_list("name")  # Tuple output
    restaurant = Restaurant.objects.values_list("name", flat=True)  # List output
```

#### Key Concepts:
- `values_list()`: Returns tuples or flat lists
- More memory-efficient than full model instances
- Quick data extraction

## 6. Aggregate and Annotate

### `index_aggregate()`
```python
def index_aggregate(request):
    ret_count = Restaurant.objects.count()
    rest_avg = Rating.objects.aggregate(avg=Avg("rating"))
    sales = Sale.objects.filter(datetime__gte=one_month_ago).aggregate(
        min=Min("income"), max=Max("income"), avg=Avg("income"), sum=Sum("income")
    )
```

#### Key Concepts:
- Perform calculations directly in the database
- Aggregate functions: Count, Avg, Min, Max, Sum
- Filter before aggregation for precise calculations

### `index_annotate()`
```python
def index_annotate(request):
    restaurant = Restaurant.objects.annotate(name_len=Length("name"))
    
    # Complex annotation with concatenation
    concatenation = Concat(
        "name",
        Value(" [Rating: "),
        Avg("ratings__rating"),
        Value("]"),
        output_field=CharField(),
    )
    rest = Restaurant.objects.annotate(message=concatenation)
```

#### Key Concepts:
- Add computed fields to QuerySet
- Perform calculations and transformations
- Useful for complex reporting and analysis

## Best Practices
1. Always use `select_related()` and `prefetch_related()` to minimize queries
2. Use `values()` and `values_list()` for lightweight data retrieval
3. Perform calculations in the database with `aggregate()` and `annotate()`
4. Be mindful of memory usage and query performance

## Performance Tips
- Profile your queries using Django Debug Toolbar
- Use `explain()` to understand query execution
- Cache complex querysets when possible
- Minimize database hits by fetching related data efficiently

