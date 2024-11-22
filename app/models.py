from django.db import models


class AbstractBaseModel(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        abstract = True


class BaseModel(AbstractBaseModel):
    pass


class BaseProxyModel(BaseModel):
    class Meta:
        proxy = True  # model which subclasses another model will be treated as a proxy model


class OneModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    age = models.IntegerField(default=10)

    class Meta:
        # a human readable name for Model
        verbose_name = "OneModel"

        # used to change the order of your model fields.
        ordering = ["-title"]

        #  Extra permissions to enter into the permissions table when creating this object.
        # Add, change, delete and view permissions are automatically created for each model.*/
        permissions = [
            ("can_publish", "Can publish OneModel"),
            ("can_archive", "Can archive OneModel"),
        ]

        #  overwrite the table name by using db_table in meta class.
        db_table = "one"

        # returns the latest object in the table based on the given field,
        get_latest_by = "title"


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    published_date = models.DateField(auto_now=True)
    owner = models.ForeignKey(Author, on_delete=models.CASCADE,related_name='book_author')

    def __str__(self):
        return f"{self.name}--{self.owner.name}"
