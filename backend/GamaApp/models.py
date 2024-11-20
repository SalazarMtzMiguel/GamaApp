from django.db import models

# Create your models here.

class Car(models.Model):
    title = models.TextField(max_length=250)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.FloatField()
    is_new = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name