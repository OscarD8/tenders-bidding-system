from django.shortcuts import render, get_object_or_404

from supply_chain.models import Council, Project

def all_councils(request):
    councils = Council.objects.all()

    context = {
        'councils': councils,
    }

    return render(request, 'supply_chain/all_councils_list.html', context)

def all_projects(request):
    return render(request, 'supply_chain/all_projects_list.html')

def project_detail(request, project_id):
    return render(request, 'supply_chain/project_detail.html')


def council_detail(request, council_id):
    return render(request, 'supply_chain/council_detail.html')