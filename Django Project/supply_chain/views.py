from django.http import HttpResponse
from django.shortcuts import render

from supply_chain.models import Council


def hello_world_index(request):
    return HttpResponse("Hello World! This is the main index of the Suppy Chain project")


def all_councils(request):
    councils = Council.objects.all()

    context = {
        'councils': councils,
    }

    return render(request, 'supply_chain/all_councils_list.html', context)

