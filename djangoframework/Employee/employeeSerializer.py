from rest_framework import serializers
from .models import Employee,Department

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeSerializerMethod(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    department = serializers.CharField(max_length=50)
    designation = serializers.CharField(max_length=50)
    salary = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_joined = serializers.DateField(read_only=True)
    is_active = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return Employee.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'