from django.db import models

# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=100,db_index=True,unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'

class Product(models.Model):

    name = models.CharField(max_length=100,db_index=True,unique=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'products'


class Order(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    total = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'orders'


