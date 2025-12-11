from django import forms
from .models import Council

class CouncilFilterForm(forms.Form):
    # Keyword Search (e.g. "Leeds") - naming the textbook 'q'
    q = forms.CharField(
        required=False,
        label='Find Authority',
        widget=forms.TextInput(attrs={
            'class': 'focus-input',
            'placeholder': 'Name or Contact...',
            'autocomplete': 'off',
            'aria-label': 'Search councils'
        })
    )

    # Region Dropdown - references by name 'region'
    region = forms.ChoiceField(
        choices=[('', 'All Regions')] + Council.Region.choices, # Add "All" option manually
        required=False,
        label='Region',
        widget=forms.Select(attrs={
            'class': 'focus-input cursor-pointer appearance-none pr-10 text-ellipsis'
        })
    )

class ProjectFilterForm(forms.Form):
    # Keyword Search Field
    q = forms.CharField(
        required=False,
        label='Keywords',
        widget=forms.TextInput(attrs={
            'class': 'focus-input',
            'placeholder': 'Solar, Roof, etc...',
            'autocomplete': 'off',
            'aria-label': 'Search projects by keywords'
        })
    )

    # Council Dropdown Field
    council = forms.ModelChoiceField(
        queryset=Council.objects.all(), # Populates the dropdown automatically
        required=False,
        label='Council',
        empty_label="All Authorities", # The default "Select All" option
        to_field_name="slug",
        widget=forms.Select(attrs={
            'class': 'focus-input cursor-pointer appearance-none pr-10 text-ellipsis'
            # Note: appearance-none is needed to hide the default browser arrow so the SVG works
        })
    )