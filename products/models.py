from django.db import models

class Product(models.Model):
    name= models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.name 

# Create your models here.
