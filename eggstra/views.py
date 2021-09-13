from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from django.db.models import Sum


from .models import EggsAvailable
# Create your views here.



# def index(request):
#     total_eggs = EggsAvailable.objects.aggregate(Sum('gather_amount'))['gather_amount__sum']
#     return HttpResponse(f"There are {total_eggs} eggs available.")

def index(request) -> HttpResponse: 
    context = { 
        'total_eggs': EggsAvailable.objects.aggregate(Sum('amount'))['amount__sum'],
        'eggs_available_collection': EggsAvailable.objects.order_by('-created_on')
    }
    return render(request, 'eggstra/index.html', context)
    #  return HttpResponse(f"There are {total_eggs} eggs available.")

def details(request, egg_available_id: int) -> HttpResponse: 
    context = { 
        'selected_eggs': get_object_or_404(EggsAvailable, pk=egg_available_id)
    }
    return render(request, 'eggstra/details.html', context)

def pickup(request, egg_available_id: int) -> HttpResponse: 
    context = { 
        'selected_eggs': get_object_or_404(EggsAvailable, pk=egg_available_id)
    }
    return render(request, 'eggstra/details.html', context)

def remove(request, egg_available_id: int) -> HttpResponse: 
    context = { }
    return render(request, 'eggstra/details.html', context)

def add(request, egg_available_id: int) -> HttpResponse: 
    context = {} 
    return render(request, 'eggstra/add.html', context)