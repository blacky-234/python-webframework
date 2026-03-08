from django.db import models
from django.db.models import Subquery,OuterRef, F, ExpressionWrapper,Sum
from django.db.models.functions import Coalesce

# Create your models here.


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CategoryQuerySet(models.QuerySet):

    def with_inventory_data(self):
        return self.annotate(
            total_stock=Coalesce(Sum('products__stock'), 0)
        )

class Category(models.Model):

    name = models.CharField(max_length=100,db_index=True,unique=True)

    objects_anontation = CategoryQuerySet.as_manager()

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


class Order(TimeStampedModel):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    total = models.FloatField(null=True)


    class Meta:
        db_table = 'orders'
