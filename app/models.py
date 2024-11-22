from django.db import models


class AbstractBaseModel(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        abstract = True
        proxy = True  # model which subclasses another model will be treated as a proxy model


class OneModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        # a human readable name for Model
        verbose_name = "OneModel"

        # used to change the order of your model fields.
        ordering = [-1]

        #  Extra permissions to enter into the permissions table when creating this object.
        # Add, change, delete and view permissions are automatically created for each model.*/
        permissions = []

        #  overwrite the table name by using db_table in meta class.
        db_table = "one"

        # returns the latest object in the table based on the given field,
        get_latest_by = "title"
