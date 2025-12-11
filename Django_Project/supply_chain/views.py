from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from supply_chain.forms import ProjectFilterForm, CouncilFilterForm
from supply_chain.models import Council, Project


def all_councils(request):
    councils = Council.objects.with_counts().order_by('name')

    # Instantiate the form with GET data (or None if the page first loads)
    form = CouncilFilterForm(request.GET)

    # Apply Filters - checks invalid input, cleans that input, if user actually typed then searches rows based on Q objects.
    if form.is_valid():
        query = form.cleaned_data.get('q')
        if query:
            councils = councils.filter(
                Q(name__icontains=query) |
                Q(contact__icontains=query)
            )

        region = form.cleaned_data.get('region')
        if region:
            councils = councils.filter(region=region)

    context = {
        'councils': councils,
        'form': form,
    }

    return render(request, 'supply_chain/council/all_councils_list.html', context)


def all_projects(request):
    projects = Project.objects.all().order_by('-created_at')

    # Instantiate the form
    form = ProjectFilterForm(request.GET)

    # Apply Filters
    if form.is_valid():
        # Filter by Keyword (Title or Description)
        query = form.cleaned_data.get('q')
        if query:
            projects = projects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        # Filter by Council
        council = form.cleaned_data.get('council')
        if council:
            # Checks against the named field of a council
            projects = projects.filter(council=council)

    context = {'projects': projects, 'form': form}

    return render(request, 'supply_chain/project/all_projects_list.html', context)


def project_detail(request, council_slug, project_slug):
    project = get_object_or_404(
        Project.objects.with_financials(), # Add the annotation instruction to the queryset
        council__slug=council_slug,
        slug=project_slug
    )

    return render(request, 'supply_chain/project/project_detail.html', {'project': project})


def council_detail(request, slug):
    council = get_object_or_404(
        Council.objects.with_counts(),
        slug=slug
    )

    return render(request, 'supply_chain/council/council_detail.html', {'council': council})
