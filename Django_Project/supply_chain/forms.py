from django import forms
from .models import Council, Bid


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
    # The form fields (q and council) are all defined explicitly as attributes directly on the ProjectFilterForm class.
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


class BidForm(forms.ModelForm):
    # Meta class required to link the form to the database model
    class Meta:
        model = Bid
        fields = ['company_name', 'contact_email', 'amount']
        widgets = { # these define fields that can be looped through on a template
            'company_name': forms.TextInput(attrs={'class': 'focus-input', 'placeholder': 'Your Company Ltd'}),
            'contact_email': forms.EmailInput(attrs={'class': 'focus-input', 'placeholder': 'tenders@company.com'}),
            'amount': forms.NumberInput(attrs={'class': 'focus-input', 'placeholder': '0.00'}),
        }