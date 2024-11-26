from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Person(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    visitation = models.ManyToManyField(City, related_name="visitor")
    hometown = models.ForeignKey(City, related_name="birth", on_delete=models.CASCADE)
    living = models.ForeignKey(City, related_name="citizen", on_delete=models.CASCADE)

    def __str__(self):
        return self.firstname + self.lastname
