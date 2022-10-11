from venv import create
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import login,logout,authenticate

# Create your views here.
def index(request):
    return render(request,'index.html')

def registration(request):
    error=""#for displaying message
    if request.method == 'POST':
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        em = request.POST['email']
        pwd = request.POST['pwd']
        
        try:
            user = User.objects.create_user(first_name=fn,last_name=ln,username=em,password=pwd) #For User Model we have to write create_user
            EmployeeDetail.objects.create( user = user ,empcode=ec)
            error = "no"
        except:
            error="yes"
    return render(request,'registration.html',locals())

def emp_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['password']
        user = authenticate(username=u,password=p)
        if user:
            login(request,user)
            error = "no"
        else:
            error = "yes"
    return render(request,'emp_login.html',locals())

def emp_home(request):
    if not request.user.is_authenticated: #if user then only home page will open
        return redirect('emp_login')
    return render(request,'emp_home.html')

def Logout(request):
    logout(request)
    return redirect('index')

def profile(request):
    if not request.user.is_authenticated: #if user then only home page will open
        return redirect('emp_login')
    error=""#for displaying message
    user = request.user
    employee = EmployeeDetail.objects.get(user=user)
    if request.method == 'POST':
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        designation = request.POST['designation']
        dept = request.POST['department']
        contact = request.POST['contact']
        jdate = request.POST['jdate']
        gender = request.POST['gender']

        employee.user.first_name = fn #these fields are for updation
        employee.user.last_name = ln
        employee.empcode = ec
        employee.designation = designation
        employee.empdept = dept
        employee.contact = contact
        employee.gender = gender

        if jdate:
            employee.joiningdate = jdate
        
        try:
          employee.save()
          employee.user.save()
          error = "no"
        except:
            error="yes"
    return render(request,'profile.html',locals())