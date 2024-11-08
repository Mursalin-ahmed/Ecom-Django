from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=10)
    cate = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', default='def.png', null=True, blank=True)
    price = models.FloatField()

    def __str__(self):
        return self.name

class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(1)

    def __str__(self):
        return f'{self.user.username}s cart'