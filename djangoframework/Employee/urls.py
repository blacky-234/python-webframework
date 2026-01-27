from django.urls import path
from .views import EmployeeManagement,DepartmentManagement
from .web_views import EmployeeProject,DepartmentManagement,ProjectManagement,EmployeeData

app_name = 'Employee'

rest_api_url = [
    path('department/',DepartmentManagement.department_management, name='departmentmanagement'),
    path('modelserializer/',EmployeeManagement.employee_model, name='modelserializer'),
    path('serializermethod/',EmployeeManagement.employee_serializermethod, name='serializermethod'),
]

web_url = [
    path('',EmployeeProject.menu, name='menuindex'),
    path('department/list',DepartmentManagement.department_management, name='departlist'),
    path('project/list',ProjectManagement.project_management, name='projectlist'),
    path('project/add/employee/<int:id>',ProjectManagement.project_add_employee, name='projectaddemployee'),
    path('list',EmployeeData.employee_list, name='employeelist'),
    path('form/add',EmployeeData.employee_add_form, name='employeeform'),
]   

urlpatterns = rest_api_url+web_url
