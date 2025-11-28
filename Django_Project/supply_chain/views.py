from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from supply_chain.models import Council, Project


def all_councils(request):
    councils = (
        Council.objects
        .annotate(projects_count=Count('project'))
        .order_by('name')
    )

    context = {
        'councils': councils,
    }

    return render(request, 'supply_chain/council/all_councils_list.html', context)


def all_projects(request):
    return render(request, 'supply_chain/project/all_projects_list.html')


def project_detail(request, project_id):
    return render(request, 'supply_chain/project/project_detail.html')


def council_detail(request, slug):
    council = get_object_or_404(
        Council.objects.annotate(projects_count=Count('project')),
        slug=slug
    )

    context = {
        'council': council,
        'project_count': council.projects_count,
    }

    return render(request, 'supply_chain/council/council_detail.html', context)
