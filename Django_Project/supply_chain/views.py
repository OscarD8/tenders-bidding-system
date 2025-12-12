from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from supply_chain.forms import ProjectFilterForm, CouncilFilterForm, BidForm
from supply_chain.models import Council, Project, Requirement


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
        Project.objects.with_financials(),  # Add the annotation instruction to the queryset
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


def place_bid(request, council_slug, project_slug, requirement_slug):
    requirement = get_object_or_404(
        Requirement,
        slug=requirement_slug,
        project__slug=project_slug,
        project__council__slug=council_slug
    )

    if request.method == 'POST':
        form = BidForm(request.POST) # Instantiate Form with POST data

        if form.is_valid():
            bid = form.save(commit=False) # Create a model instance but don't save to DB yet
            bid.requirement = requirement # Add the missing ForeignKey/contextual data
            bid.save() # Save the complete object to the DB
            messages.success(request, f"Bid of £{bid.amount} submitted successfully!") # can see the message on the admin page
            return redirect('supply_chain:project_detail', council_slug=council_slug, project_slug=project_slug)
    else:
        # This handles the GET request (initial page load)
        form = BidForm()

    context = {
        'form': form,
        'requirement': requirement,
        'project': requirement.project,
        'council': requirement.project.council
    }
    return render(request, 'supply_chain/bids/bid_form.html', context)