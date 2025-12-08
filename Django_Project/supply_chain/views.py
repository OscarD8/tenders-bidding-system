from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

from supply_chain.models import Council, Project


def all_councils(request):
    councils = (
        Council.objects
        .annotate(projects_count=Count('project'))
        .order_by('name')
    )

    return render(request, 'supply_chain/council/all_councils_list.html', { 'councils': councils})


def all_projects(request):
    projects = Project.objects.all().order_by('-created_at')

    return render(request, 'supply_chain/project/all_projects_list.html', {'projects': projects})


def project_detail(request, council_slug, project_slug):
    project = get_object_or_404(Project, council__slug=council_slug, slug=project_slug)

    return render(request, 'supply_chain/project/project_detail.html', {'project': project})


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
