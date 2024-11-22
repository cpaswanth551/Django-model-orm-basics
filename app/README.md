
---

## **`OneListview`**

This view demonstrates various ORM query concepts using the `OneModel`. Below is a breakdown of each query:

### 1. **Getting All Entries**
```python
one_list = OneModel.objects.all()
```
- **Purpose:** Retrieves all records from the `OneModel`.
- **Use Case:** To fetch all entries in the table for display or processing.

---

### 2. **Filtering Based on a Specific Title**
```python
one_filter_by_title = OneModel.objects.filter(title="hello users")
```
- **Purpose:** Filters records where the `title` field matches the exact value `"hello users"`.
- **Use Case:** To find entries with a specific title.

---

### 3. **Filtering with Multiple Conditions Using `Q` Objects**
```python
one_filter_has_same_title_and_description_with_given_command = (
    OneModel.objects.filter(Q(age__gte=20) & Q(title__startswith="h")).values()
)
```
- **Purpose:** Filters records where:
  - `age` is greater than or equal to 20.
  - `title` starts with the letter `'h'`.
- **Use Case:** To handle complex queries with multiple conditions.

---

### 4. **Chaining Filter and Exclude**
```python
one_filter_with_exclude = (
    OneModel.objects.filter(title__startswith="h").exclude(age__gte=25).values()
)
```
- **Purpose:** 
  - Filters records where the `title` starts with `'h'`.
  - Excludes records where `age` is greater than or equal to 25.
- **Use Case:** To refine queries by combining inclusion and exclusion criteria.

---

### 5. **Using Aggregate Functions**
```python
one_filter_aggregate = (
    OneModel.objects.all()
    .aggregate(avg_age=Avg("age"), sum_age=Sum("age"), max_age=Max("age"))
    .values()
)
```
- **Purpose:** Calculates:
  - Average (`Avg`) age.
  - Total (`Sum`) of ages.
  - Maximum (`Max`) age from all records.
- **Use Case:** To generate summary statistics for numerical fields.

---

### 6. **Using Annotate**
```python
one_filter_annotate = OneModel.objects.annotate(avg_age=Avg("age")).values()
```
- **Purpose:** Adds an `avg_age` annotation to each record, calculating the average value of `age`.
- **Use Case:** To calculate additional fields for each row dynamically.

---

### 7. **Using Map to Process Query Results**
```python
one_map = {one.pk: {one.title, one.description} for one in one_filter_list}
```
- **Purpose:** Converts query results into a dictionary where the key is the primary key (`pk`) and the value is a set of `title` and `description`.
- **Use Case:** For creating a custom dictionary representation of query results.

---

## **`bookView`**

This view demonstrates advanced ORM operations with models like `Book` and `Author`.

### 1. **Using `select_related` for Efficient Queries**
```python
books_with_author_selectrelated = (
    Book.objects.filter(owner__name="Aswanth C P")
    .select_related("owner")
    .only("id", "name", "owner__name")
)
```
- **Purpose:** Retrieves books where the owner's name is `"Aswanth C P"`. It uses `select_related` to fetch related `owner` data in the same query and limits the fields fetched to `id`, `name`, and `owner__name`.
- **Use Case:** For optimizing queries with one-to-one or foreign key relationships.

---

### 2. **Using `prefetch_related`**
```python
author__published_book_year = (
    Author.objects.prefetch_related("book_author")
    .filter(book_author__published_date__year=2024)
    .distinct()
)
```
- **Purpose:** 
  - Prefetches books written by authors.
  - Filters authors whose books are published in the year `2024`.
  - Ensures distinct results.
- **Use Case:** To optimize queries with many-to-many or reverse foreign key relationships.

---

### 3. **Annotating Authors with Book Counts**
```python
authors_with_book_count = Author.objects.annotate(
    book_count=Count("book_author")
).prefetch_related("book_author")
```
- **Purpose:** 
  - Adds an annotation `book_count` to each author, showing the total number of books they authored.
  - Prefetches related books.
- **Use Case:** To include aggregate data in query results.

---

### 4. **Executing Raw SQL**
```python
books = Book.objects.raw("select * from app_book where name like 'b%'")
for book in books:
    print(book.name)
```
- **Purpose:** 
  - Executes a raw SQL query to fetch books whose names start with `'b'`.
  - Iterates over the raw query results.
- **Use Case:** For executing custom SQL queries not supported by ORM.

---

## **Notes**

1. **Optimization Tips:**
   - Use `select_related` and `prefetch_related` appropriately to reduce database queries.
   - Limit the fields fetched using `.only()` when the full dataset is not required.

2. **Advanced Queries:**
   - Use `Q` objects for complex filtering.
   - Use aggregate and annotate for statistical calculations and dynamic field additions.

3. **Custom Queries:**
   - For performance-critical cases, raw SQL queries can be helpful but should be used sparingly and with caution.

---

