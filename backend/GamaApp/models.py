from django.db import models

# Create your models here.


class Car(models.Model):
    title = models.TextField(max_length=250, default="Car")
    name = models.CharField(max_length=100, default="Car")
    color = models.CharField(max_length=100, default="Red")
    year = models.IntegerField(default=1800)
    price = models.FloatField(default=0.0)
    is_new = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.name} - {self.color} - {self.year} - {self.price} - {self.is_new}"
        )


class Dog(models.Model):
    name = models.CharField(max_length=100)


class Publisher(models.Model):
    name = models.TextField(max_length=300)
    address = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.address}"


class Book(models.Model):
    title = models.TextField(max_length=300)
    author = models.TextField(max_length=200)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()

    def __str__(self):
        return (
            f"{self.title} - {self.author} - {self.publisher} - {self.publication_date}"
        )

class Product(models.Model):
    name = models.TextField(max_length=200,verbose_name="nombre")
    description = models.TextField(max_length=500)
    price = models.FloatField(default=0.0)
    available = models.BooleanField(default=True)
    photo=models.ImageField(upload_to='products/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.description} - {self.price}"