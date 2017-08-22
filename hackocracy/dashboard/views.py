from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, TransactionForm
from django.contrib.auth.decorators import login_required
from .models import *


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data['username'],
                                password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    elif request.method == 'GET':
        form = LoginForm()
    return render(request, 'dashboard/login.html', {'form': form})


@login_required
def dashboard(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST);
        if form.is_valid():
            post = form.save();
            post.save();
            form_new = TransactionForm();
            return render(request,
                          'dashboard/dashboard.html',
                          {'section': 'dashboard', 'form': form_new ,'saved_success': True})
    else:
        form = TransactionForm();
        return render(request,
                      'dashboard/dashboard.html',
                      {'section':'dashboard','form':form ,'saved_success': False})

@login_required
def Transaction_history(request):
    to_trans=transactions.objects.filter(to = request.user).order_by('timestamp')

    rec = 0
    for to_t in to_trans:
        rec += to_t.amount

    from_trans = transactions.objects.filter(fro = request.user).order_by('timestamp')

    giv=0
    for from_t in from_trans:
        giv += from_t.amount

    total = rec - giv
    return render(request,
                  'dashboard/Transaction_history.html',
                  {'section':'transaction_history','to_trans':to_trans,'from_trans':from_trans,'recieved':rec,'given':giv,'sum':total})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request,
                          'dashboard/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'dashboard/register.html',
                  {'user_form': user_form})
