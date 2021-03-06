from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from .forms import CreateUserForm
from .models import *

@login_required(login_url='login')
@admin_only
def detail(request):
    customers = Customer.objects.all()

    total_customers = customers.count()

    context = {'customers':customers }
    return render(request, 'app/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    context = {'customer':customer}
    return render(request, 'app/customer.html',context)

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')


    context = {'form':form}
    return render(request, 'app/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
        
    context = {}
    return render(request, 'app/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


def userPage(request):
    context = {}
    return render(request, 'app/user.html', context)

@login_required(login_url='login')
@admin_only
def home(request):
    context={}
    return render(request,'app/detail.html',context)