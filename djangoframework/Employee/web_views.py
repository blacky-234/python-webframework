from django.shortcuts import render,redirect
from .models import Employee,Department,Project,Profile
from django.db import transaction
import asyncio
from asgiref.sync import sync_to_async

class EmployeeProject:

    def menu(request):
        return render(request, 'indexMenu.html')


class DepartmentManagement:

    def department_management(request):
        context = {}
        if request.method == 'GET':
            context['departments'] = Department.objects.all()
            return render(request, 'department/departmentlist.html',context)

class ProjectManagement:

    def project_management(request):
        context = {}
        if request.method == 'GET':
            context['projects'] = Project.objects.all()
            return render(request, 'project/projectlist.html',context)
    
    async def project_add_employee(request,id):
        context = {}
        if request.method == 'GET':
            employee_task = sync_to_async(Employee.objects.get)(id=id)
            projects_task = sync_to_async(list)(Project.objects.all())

            employee, projects = await asyncio.gather(
                employee_task,
                projects_task
            )
            context['employees'] = employee
            context['projects'] = projects
            return render(request, 'project/projectaddemployee.html',context)
        elif request.method == 'POST':
            try:
                pro_id = int(request.POST.get('projectid'))
                d = Project.objects.get(id=pro_id)
                Employee.objects.get(id=id).projects.add(d)
                return redirect('Employee:employeelist')
            except Project.DoesNotExist:
                return redirect('Employee:employeelist')
        

class EmployeeData:

    def employee_list(request):
        context = {}
        if request.method == 'GET':
            context["emp"] = Employee.objects.select_related("department","profile").prefetch_related("projects").all()
            return render(request, 'employee/employeelist.html',context)
    

    def employee_add_form(request):
        context = {}
        if request.method == 'GET': 
            context['departments'] = Department.objects.all()         
            return render(request, 'employee/employeeaddform.html',context)
        elif request.method == 'POST':
            try:
                with transaction.atomic():
                    name = request.POST.get('empname','').strip()
                    email = request.POST.get('empemail','').strip()
                    department = int(request.POST.get('empdep'))
                    salry = request.POST.get('empsalary')
                    address = request.POST.get('empaddress','').strip()
                    phone = request.POST.get('empphone','').strip()
                    em_phone = request.POST.get('empcontact','').strip()

                    if not name or Employee.objects.filter(email=email).exists():
                        return redirect('Employee:employeelist')
                    d = Department.objects.get(id=department)
                    print(f"department : {d.pk}")
                    emp = Employee.objects.create(
                                            name=name,
                                            email=email,
                                            department=d,
                                            salary=salry
                                        )

                    Profile.objects.create(
                        employee=emp,
                        address=address,
                        phone=phone,
                        emergency_contact=em_phone
                    )
                    return redirect('Employee:employeelist')
            except Department.DoesNotExist:
                return redirect('Employee:employeelist')
            except Exception as e:
                print(e)
                return redirect('Employee:employeelist')