from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password    #check_password
from .models import *
from django.contrib.auth import login, logout, authenticate
from .forms import previewForm, EmployeeForm
from .models import Day, TimeSlot, Schedule
from django.contrib.auth.hashers import check_password
from .forms import EmployeeWorkDetailForm

import datetime
import bcrypt



#Create your views here
def landpage(request):
    return render(request, 'landpage.html')



def registration(request):

    error = ""
    form = EmployeeForm()
    # print(request.POST)

    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            error = "Passwords do not match"
        else:
            form = EmployeeForm(request.POST)
            if form.is_valid():
                # Get the password from the form
                password = form.cleaned_data.get('password')
                # Hash the password
                hashed_password = make_password(password)
                # Update the form's password field with the hashed password
                form.instance.password = hashed_password
                form.save()
                # Add a success message
                messages.success(request, 'Registration successful!')
                return redirect('/')
            else:
                print("Form is not valid. Errors:")
                print(form.errors)
                # error = "Error in submitting form"
        
    return render(request, 'registration.html', {'form': form, 'error': error})

def logout_view(request):
    # Clear session data
    request.session.flush()
    # Redirect to a login page or any other desired page
    return redirect('/employeelogin')


def employeelogin(request):

    error = ""
    if request.method == "POST":
        employeId = request.POST.get('employeId')
        password = request.POST.get('password')

        employee = EmployeeDetail.objects.filter(empID=employeId).first()

        print(employee)
        print(employee.password)
        print(employee.fullName)
        print(employee.isAdmin)
        # print(check_password(password, employee.password))

        if employee is not None:
            # Check if the password matches
            if check_password(password, employee.password):
                # Password matches, log in the employee
                request.session.create()  # Create a new session
                request.session['employeId'] = employeId  # Set user_id in session
                request.session['fullName'] = employee.fullName 
                # login(request, employee)
                # Redirect to the dashboard or any other page
                if (employee.isAdmin):
                    return redirect('/adminlogin')
                return redirect('/employeehome')  # Change 'dashboard' to your desired URL name
            else:
                error = "Invalid password. Please try again."
        else:
            error = "Invalid employeId. Please try again."

    return render(request, 'employeelogin.html',  {'error': error})

def employeehome(request):

    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    weekdays = [start_of_week + datetime.timedelta(days=i) for i in range(5)]

    days = Day.objects.filter(day_of_week__in=weekdays).order_by('day_of_week')
    time_slots = TimeSlot.objects.all().order_by('start_time')

    return render(request, 'employeehome.html', {'days': days, 'time_slots': time_slots, 'weekdays': weekdays})


def employeepreview(request):
    return render(request, 'employeepreview.html')


def Form(request):
    if request.method == 'POST':
        form = previewForm(request.POST)
        if 'preview' in request.POST:  # Check if the Preview button was clicked
            if form.is_valid():
                return render(request, 'employeepreview.html', {'form_data': form.cleaned_data})
        elif 'save' in request.POST:  # Check if the Save button was clicked
            if form.is_valid():
                form.save()
                return HttpResponse('/success/')
        else:
            form = previewForm()
    return render(request, 'employeehome.html', {'form': form})

# def adminlogin(request):
#     return render(request, 'adminlogin.html')

def adminlogin(request):
    employees = EmployeeWorkDetail.objects.all()
    return render(request, 'adminlogin.html', {'employees': employees})

def employeedetail(request, name):
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    weekdays = [start_of_week + datetime.timedelta(days=i) for i in range(5)]

    days = Day.objects.filter(day_of_week__in=weekdays).order_by('day_of_week')
    time_slots = TimeSlot.objects.all().order_by('start_time')

    employee = EmployeeWorkDetail.objects.get(name=name)

    return render(request, 'employeedetail.html', { 'employee': employee, 'data_fetched': EmployeeWorkDetail.objects.filter(name=name).exists(), 'days': days, 'time_slots': time_slots, 'weekdays': weekdays })

# def employee_home(request):
#     print('Hello')
#     if request.method == 'POST':
#         form = EmployeeWorkDetailForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/employeehome')
#     else:
#         if EmployeeWorkDetail.objects.exists():
#             employee_detail = EmployeeWorkDetail.objects.latest('assigned_on')
#             print(employee_detail.is_completed())
#             if employee_detail.is_completed():
#                 form = EmployeeWorkDetailForm()
#             else:
#                 form = EmployeeWorkDetailForm(instance=employee_detail)
#         else:
#             form = EmployeeWorkDetailForm()


#     return render(request, 'employeehome.html', {'form': form,  'data_fetched': employee_detail is not None })

def employee_home(request):
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    weekdays = [start_of_week + datetime.timedelta(days=i) for i in range(5)]

    days = Day.objects.filter(day_of_week__in=weekdays).order_by('day_of_week')
    time_slots = TimeSlot.objects.all().order_by('start_time')

    employe_id = request.session.get('employeId')
    fullName = request.session.get('fullName')
    print('session', employe_id, fullName)

    if request.method == 'POST':
        if EmployeeWorkDetail.objects.filter(name=fullName).exists():
            employee_detail = EmployeeWorkDetail.objects.filter(name=fullName).latest('assigned_on')
            form_data = {
                'name': employee_detail.name,
                'designation': employee_detail.designation,
                'project': employee_detail.project,
                'assigned_on': employee_detail.assigned_on,
                'completion_date': request.POST.get('completion_date')
            }
            form = EmployeeWorkDetailForm(form_data, instance=employee_detail)
        else:
            form = EmployeeWorkDetailForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('/employeehome')
        else:
            print(form.errors)
    else:
        if EmployeeWorkDetail.objects.filter(name=fullName).exists():
            employee_detail = EmployeeWorkDetail.objects.filter(name=fullName).latest('assigned_on')
            form = EmployeeWorkDetailForm(instance=employee_detail)
            print('here')
        else:
            form = EmployeeWorkDetailForm()
            print('there')

    return render(request, 'employeehome.html', { 'form': form, 'data_fetched': EmployeeWorkDetail.objects.filter(name=fullName).exists(), 'days': days, 'time_slots': time_slots, 'weekdays': weekdays })





# password = b"pwd"
# hashedPwd = bcrypt.hashpw(password, bcrypt.gensalt())
        
# hashed_password = make_password(pwd)  # Hash the password
# User.objects.create(username=ec, password=hashed_password)

# user = User.objects.create_user(full_name=fn, phone_number=ph , dob=dob, doj=doj, gender=gender, empID=ec) #email_ID=em, password=hashed_password)
# EmployeeDetail.objects.create(user = user, empID=ec)