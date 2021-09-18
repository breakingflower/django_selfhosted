from eggstra.forms import PostForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader

from django.db.models import Sum


from .models import EggsAvailable
# Create your views here.



# def index(request):
#     total_eggs = EggsAvailable.objects.aggregate(Sum('gather_amount'))['gather_amount__sum']
#     return HttpResponse(f"There are {total_eggs} eggs available.")

def overview(request) -> HttpResponse: 
    context = { 
        'total_eggs': EggsAvailable.objects.aggregate(Sum('amount'))['amount__sum'],
        'eggs_available_collection': EggsAvailable.objects.order_by('-created_on')
    }
    return render(request, 'eggstra/overview.html', context)

def pickup(request, egg_available_id: int) -> HttpResponse: 
    context = { 
        'selected_eggs': get_object_or_404(EggsAvailable, pk=egg_available_id)
    }
    return render(request, 'eggstra/pickup.html', context)

def remove(request, egg_available_id: int) -> HttpResponse: 
    context = { }
    return render(request, 'eggstra/overview.html', context)

def logout(request): 
    return render(request, '')

def post(request) -> HttpResponse: 
    if request.method == 'POST' and request.user.is_authenticated():
        form = PostForm(request.POST)
        if form.is_valid():

            # extract from form
            amount = form.cleaned_data['amount']
            notes = form.cleaned_data['notes']

            # create new entry for db
            eggs_available = EggsAvailable( 
                amount = amount,
                notes = notes,
                created_by = request.user
            )
            
            # post in db
            eggs_available.save()

            # redirect to index
            return redirect('eggstra:overview')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PostForm()

    return render(request, 'eggstra/post.html',  {'form': form})

def register(request): 
    return render(request, 'eggstra/register.html')

def userprofile(request): 
    return render(request, 'eggstra/userprofile.html')

# @login_required
# @transaction.atomic
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, _('Your profile was successfully updated!'))
#             return redirect('settings:profile')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'profiles/profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })