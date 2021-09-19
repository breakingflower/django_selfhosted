from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db.models import Sum


from .models import EggPost
from .forms import EggPostForm, RegisterForm, UserForm, ProfileForm
# Create your views here.

def overview(request) -> HttpResponse: 
    context = { 
        'total_eggs': EggPost.objects.aggregate(Sum('amount'))['amount__sum'],
        'eggposts': EggPost.objects.order_by('date')
    }
    return render(request, 'eggstra/overview.html', context)

@login_required(redirect_field_name='next', login_url='login')
def pickup(request, eggpost_id: int) -> HttpResponse: 
    context = { 
        'post': get_object_or_404(EggPost, pk=eggpost_id)
    }
    return render(request, 'eggstra/pickup.html', context)

@login_required(redirect_field_name='next', login_url='login')
def eggpost_delete(request, eggpost_id: int) -> HttpResponse: 
    eggpost = EggPost.objects.get(pk=eggpost_id)
    if request.user == eggpost.user: 
        messages.add_message(request, messages.SUCCESS, f'Je post van {eggpost.date.strftime("%d-%m-%Y")} is verwijderd.')
        eggpost.delete()
    else: 
        messages.add_message(request, messages.ERROR, f'Je bent niet de auteur van deze post, je kan dit niet verwijderen.')
    return redirect('eggstra:overview')

@login_required(redirect_field_name='next', login_url='login')
def eggpost_update(request, eggpost_id: int) -> HttpResponse: 
    eggpost = EggPost.objects.get(pk=eggpost_id)
    
    if request.user == eggpost.user: 
        if request.method == 'POST':
            form = EggPostForm(request.POST, instance=eggpost)
            if form.is_valid():
                form.save() 
                messages.add_message(request, messages.SUCCESS, f'Je post is geupdate!')
                return redirect('eggstra:overview')
        else:
            form = EggPostForm(instance=eggpost)
    return render(request, 'eggstra/eggpost.html',  {'form': form, 'action': f"/eggstra/{eggpost.id}/update/"})

@login_required(redirect_field_name='next', login_url='login')
def eggpost(request) -> HttpResponse: 
    if request.method == 'POST':
        form = EggPostForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False) 
            form.user = request.user
            form.save() 

            # flash message
            if form.amount == 1: 
                messages.add_message(request, messages.SUCCESS, f'Thanks {request.user}! Je eitje staat er bij.')
            else: 
                messages.add_message(request, messages.SUCCESS, f'Thanks {request.user}! Je {form.amount} eitjes staan er bij.')

            # redirect to index
            return redirect('eggstra:overview')
    else:
        form = EggPostForm()
    return render(request, 'eggstra/eggpost.html',  {'form': form, 'action': "/eggstra/eggpost/"})

def register(request) -> HttpResponse: 
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            # flash message
            messages.add_message(request, messages.SUCCESS, f'Thanks! Je account is nu actief.')

            return redirect('login')
    else: 
        form = RegisterForm() 
    return render(request, 'eggstra/register.html', {'form': form})

@login_required(redirect_field_name='next', login_url='login')
def user_delete(request): 
    pass

@login_required(redirect_field_name='next', login_url='login')
def profile(request): 
    if request.method == "POST": 
        userform = UserForm(request.POST, instance=request.user) 
        profileform = ProfileForm(request.POST, instance=request.user.profile)

        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save() 
            
            # flash message
            messages.add_message(request, messages.SUCCESS, f'Account details geupdate.')
            return redirect('eggstra:overview')
    else: 
        userform = UserForm(instance=request.user)
        profileform = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/profile.html', {'userform': userform, 'profileform': profileform}) # {'userform': userform, 'profileform': profileform})
