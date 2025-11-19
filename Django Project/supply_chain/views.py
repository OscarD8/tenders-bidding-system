from django.http import HttpResponse
from django.shortcuts import render

from supply_chain.models import Council, Project


def home(request):
    return render(request, 'supply_chain/index.html')

def all_councils(request):
    councils = Council.objects.all()

    context = {
        'councils': councils,
    }

    return render(request, 'supply_chain/all_councils_list.html', context)

def project_list(request):
    """
        Renders the Projects List Page (project_list.html)
        Handles Search and Council filtering.
    """
    projects = Project.objects.select_related('council').all().order_by('-created_at')
    councils = Council.objects.all()  # For the dropdown filter

    # 1. Handle Keyword Search
    query = request.GET.get('q')
    if query:
        projects = projects.filter(title__icontains=query) | projects.filter(description__icontains=query)

    # 2. Handle Council Filter
    council_id = request.GET.get('council')
    if council_id:
        projects = projects.filter(council_id=council_id)

    context = {
        'projects': projects,
        'councils': councils,
    }
    return render(request, 'supply_chain/project_list.html', context)