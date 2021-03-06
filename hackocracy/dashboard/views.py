from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm,TransactionForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import views as auth_views
import json
from django.contrib import messages
from block.views import get_genesis_block, Block, mine
from block.models import BlockChain
from django.conf import settings
from block.views import verify_chain


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
def Transaction_history(request):

    to_trans = Exchanges.objects.filter(to=request.user).order_by('timestamp')
    rec = sum([x.amount for x in to_trans])

    from_trans = Exchanges.objects.filter(fro=request.user).order_by('timestamp')
    giv = sum([x.amount for x in from_trans])

    total = rec - giv
    return render(request,
                  'dashboard/Transaction_history.html',
                  {'section': 'transaction_history',
                   'to_trans': to_trans,
                   'from_trans': from_trans,
                   'recieved': rec,
                   'given': giv,
                   'sum': total})


@login_required
def dashboard(request):

    # Try to load the blockchain
    q = BlockChain.objects.all()
    request.session['blockchain'] = []
    if q.exists():
        for json_block in q:
            request.session['blockchain'].append(json_block.block)
    else:
        # Initialize a blockchain when the user logs in
        request.session['blockchain'] = [Block.toJSON(get_genesis_block())]
    # print all the blocks in the blockchain
    # for block in request.session['blockchain']:
    #     print 'after login'
    #     print block

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        # print(type(request.user.username))
        # print(form["to"].value() == request.user.username)
        # print(form["fro"].value() == request.user.username)
        if form.is_valid()and(form["to"].value()==request.user.username or form["fro"].value()==request.user.username ):
            post = form.save()
            post.save()
            form_new = TransactionForm()
            messages.success(request, 'Last Transaction Saved Successfully!')
            return render(request,
                          'dashboard/dashboard.html',
                          {'section': 'dashboard', 'form': form_new, 'img':request.user.profile.party_image})
        else:
            form = TransactionForm()
            messages.error(request, 'Enter a transaction pertaining to the current user!')
            return render(request,
                          'dashboard/dashboard.html',
                          {'section': 'dashboard', 'form': form, 'img': request.user.profile.party_image})
    else:
        form = TransactionForm()
        return render(request,
                      'dashboard/dashboard.html',
                      {'section':'dashboard','form':form, 'img':request.user.profile.party_image})


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
            # Create the user profile
            profile = Profile.objects.create(user=new_user,
                                             political_party=user_form.cleaned_data['political_party'],
                                             party_image=user_form.cleaned_data['party_image'])
            # Works without this save line somehow
            profile.save()
            return render(request,
                          'dashboard/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'dashboard/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'dashboard/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def custom_logout(request):
    mine(request, logging_out=True)
    # First delete all the entries from the table
    BlockChain.objects.all().delete()
    # Replace with the current blockchain
    for block in request.session['blockchain']:
        q = BlockChain(block=block)
        q.save()
        # print 'while logout the session is :'
        # print block
    return auth_views.logout(request)


def send_blockchain(request):

    blockchain = []

    full_chain = BlockChain.objects.all()
    for x in full_chain:
        blockchain.append(x.block)

    # check own blockchain before sending if its not valid then then send blank
    if not verify_chain(blockchain):
        blockchain = []

    data = json.dumps(blockchain)
    return HttpResponse(data, content_type='application/json')


def all_transaction(request):

    mine(request)

    to_trans =[]
    i=0
    for block in request.session['blockchain']:
        q = json.loads(block)
        if(i!=0):
            ob=json.loads(q["data"])
            for datas in ob:
                t = []
                t.append(datas["to"])
                t.append(datas["fro"])
                t.append(datas["amount"])
                t.append(datas["timestamp"])
                to_trans.append(t)
        i=i+1
    return render(request,
                  'dashboard/all_transaction.html',
                  {'section': 'all_transaction',
                   'to_trans': to_trans,})
