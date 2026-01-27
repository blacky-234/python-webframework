from django.db import models

# Create your models here.

class Department(models.Model):

    name = models.CharField(max_length=100,unique=True,db_index=True)
    location = models.CharField(max_length=100,blank=True,null=True)

    class Meta:
        db_table = 'department'
        ordering = ['id']


class Project(models.Model):

    name = models.CharField(max_length=100,unique=True,db_index=True)
    deadline = models.DateField(blank=True,null=True)

    class Meta:
        db_table = 'project'
        ordering = ['name']

    def __str__(self):
        return self.name

class Employee(models.Model):
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True,db_index=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    projects = models.ManyToManyField(Project, related_name='employees')
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'employee'
        ordering = ['name']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'


class Profile(models.Model):

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    emergency_contact = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'profile'
    
    def __str__(self):
        return f"{self.employee.name}'s Profile"