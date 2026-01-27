from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .employeeSerializer import EmployeeSerializer, EmployeeSerializerMethod, DepartmentSerializer
from .models import Employee,Department

# Create your views here.
from faker import Faker

class DepartmentManagement:

    @api_view(['GET'])
    def department_management(request):
        if request.method == 'GET':
            departments = Department.objects.all()
            serializer = DepartmentSerializer(departments, many=True)
            return Response(serializer.data)

class EmployeeManagement:


    @api_view(['GET','POST'])
    def employee_model(request):
        if request.method == 'GET':
            employees = Employee.objects.all()
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            print("what is data : ", request.data)
            data = {
                    "name": request.data['name'],
                    "email": request.data['email'],
                    "department": request.data["department"],
                    "designation": request.data["designamtion"],
                    "salary": request.data["salary"],
                    "is_active": request.data["isactive"]
                }
            serializer = EmployeeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(request.data)
    
    @api_view(['GET','POST'])
    def employee_serializermethod(request):
        if request.method == 'GET':
            employees = Employee.objects.all()
            serializer = EmployeeSerializerMethod(employees, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            data = {
                'name' : request.data['name'],
                'email' : request.data['email'],
                'department' : request.data['department'],
                'designation' : request.data['designation'],
                'salary' : request.data['salary'],
                'is_active' : request.data['isactivate']
            }
            serializer = EmployeeSerializerMethod(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(status=200, data=data)
