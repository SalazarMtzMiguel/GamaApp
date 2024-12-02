from django.db import models
from django.contrib.auth.models import User, AbstractUser

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
    
class Simulation(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='simulations/')
    users_with_access = models.ManyToManyField(User, related_name='allowed_simulations')

    def __str__(self):
        return self.name

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_profile',default=3)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    maternal_last_name = models.CharField(max_length=150, blank=True, null=True)
    accepted_terms = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    # Other fields for the user profile

    def __str__(self):
        return self.user.username