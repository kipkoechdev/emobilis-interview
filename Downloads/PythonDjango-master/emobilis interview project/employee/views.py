from django.shortcuts import render, redirect
from employee.forms import EmployeeForm
from employee.models import Employee
from django.http import HttpResponse, JsonResponse
from django_daraja.mpesa.core import MpesaClient



# Create your templates here.
# .save() is the ORM equivalent of the SQL insert to statement.
def emp(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                employee = form.save()
                return JsonResponse({
                    'success': True,
                    'employee': {
                        'id': employee.id,
                        'name': employee.employee_name,
                        'email': employee.employee_email,
                        'contact': employee.employee_contact,
                    }
                })
            except:
                return JsonResponse({'success': False})
    else:
        form = EmployeeForm()
    return render(request,'index.html',{'form':form})

# .all() is the ORM equivalent of the SQL statement "SELECT * FROM tablename"
def show(request):
    employees = Employee.objects.all().values()  #return a dict
    # we need to loop the employees dict
    employee_list = []
    for employee in employees:
        employee_dict = {
            'id': employee['id'],
            'name': employee['employee_name'],
            'email': employee['employee_email'],
            'contact': employee['employee_contact'],
        }
        employee_list.append(employee_dict)
    return JsonResponse({
        'success': True,
        'employees': employee_list
    })


# .get is the ORM equivalent of the SQL statement "SELECT * FROM tablename WHERE id = ? "
# method update carries the update process for a single record
def edit(request, id):
    employee = Employee.objects.get(id=id)
    return JsonResponse({
        'success': True,
        'employee': {
            'id': employee.id,
            'name': employee.employee_name,
            'email': employee.employee_email,
            'contact': employee.employee_contact,
        }
    })
def checkout(request, id):
    employee = Employee.objects.get(id=id)
    return JsonResponse({
        'success': True,
        'employee': {
            'id': employee.id,
            'name': employee.employee_name,
            'email': employee.employee_email,
            'contact': employee.employee_contact,
        }
    })
def update(request, id):
    employee = Employee.objects.get(id=id)
    form = EmployeeForm(request.POST, instance = employee)
    if form.is_valid():
        employee = form.save()
        return JsonResponse({
            'success': True,
            'employee': {
                'id': employee.id,
                'name': employee.name,
                'email': employee.email,
                'contact': employee.contact
            }
        })
    return JsonResponse({'success': False})
def checkoutpay(request):
    if request.method == "POST":
        # capture input
        amount = request.POST.get('amount')
        phoneNumber = request.POST.get('id_employee_contact')
        # Check if phoneNumber and amount exist and have valid values
        if not phoneNumber or not phoneNumber.isdigit():
            return HttpResponse('Invalid phone number')
        if not amount or not amount.isdigit():
            return HttpResponse('Invalid amount')
        # Do something with the amount, like create a payment object or update the employee salary
        cl = MpesaClient()
        phone_number = int(phoneNumber)
        amount = int(amount)
        account_reference = 'JOSEPH ENTERPRISES'
        transaction_desc = 'paying shoes'
        callback_url = 'https://api.darajambili.com/express-payment'
        response = cl.stk_push(str(phone_number), amount, account_reference, transaction_desc, callback_url)
        return HttpResponse(response)
    else:
        form = EmployeeForm()
    return render(request, 'checkout.html', {'form': form})


# .delete() is the ORM equivalent of the statement SQL : " DELETE FROM tablename WHERE id = ? "
def destroy(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return JsonResponse({'success': True, 'message': 'data has been deleted.'})





























