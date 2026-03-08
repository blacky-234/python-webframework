from rest_framework import serializers
from .models import Category

class CategoryInventorySerializer(serializers.ModelSerializer):
    total_stock = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ["id", "name", "total_stock"]