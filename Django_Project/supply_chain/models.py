from django.db import models
from django.db.models import Sum, F, Value, DecimalField, Count
from django.db.models.functions import Coalesce
from autoslug import AutoSlugField
from django.core.validators import RegexValidator

class CouncilManager(models.Manager):
    def with_counts(self):
        return self.get_queryset().annotate(
            projects_count=Count('project')
        )


class Council(models.Model):
    name = models.CharField(max_length=100)

    contact = models.CharField(max_length=100)
    contact_email = models.EmailField()

    slug = AutoSlugField(populate_from='name', always_update=True, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CouncilManager()

    class Meta:
        verbose_name_plural = "Councils"
        ordering = ['name']

    def __str__(self):
        return f'{self.name} Council'


class ProjectManager(models.Manager):
    def with_financials(self):
        """
        Annotates the query with 'total_allocated' and 'retained_budget'
        calculated directly in the database.
        """
        return self.get_queryset().annotate(
            # Coalesce ensures if there are NO requirements, we get 0 instead of None (null)
            total_allocated=Coalesce(
                Sum('requirements__estimated_value'),
                Value(0, output_field=DecimalField())
            ),

            # Calculate Retained: Budget - Allocated
            retained_budget=F('budget') - F('total_allocated')
        )


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = AutoSlugField(populate_from='title', unique_with=['council'], always_update=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2)

    council = models.ForeignKey(Council, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProjectManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Projects"

    def __str__(self):
        return f'{self.title}'

    @property # Treat this function like a variable. Don't make me use brackets () to call it.
    def percentage_allocated(self): # this is like an interface
        if self.budget == 0:
            return 0

        # 1. Try to get the pre-calculated value from our custom manager (Fast)
        allocated = getattr(self, 'total_allocated', None)

        # 2. Fallback: If 'total_allocated' is missing (e.g. accessed via Admin or basic .get())
        # we must query the database now to ensure the property doesn't break.
        if allocated is None:
            allocated = self.requirements.aggregate(total=Sum('estimated_value'))['total'] or 0

        return (allocated / self.budget) * 100


class Requirement(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open for Bidding'),
        ('REVIEW', 'Under Review'),
        ('CLOSED', 'Closed / Awarded'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="requirements")
    cpv_code = models.CharField(
        max_length=10,  # Exact length of a CPV code
        help_text="Format: 8 digits, a hyphen, and a check digit (e.g. 45233120-6)",
        validators=[
            RegexValidator(
                regex=r'^\d{8}-\d$',  # The Pattern: 8 numbers, 1 dash, 1 number
                message="CPV code must be in the format XXXXXXXX-Y (e.g. 45233120-6)"
            )
        ]
    )
    title = models.CharField(max_length=200, help_text="e.g. Road Resurfacing")
    description = models.TextField()

    estimated_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="The ceiling budget for this specific package"
    )
    deadline = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')

    class Meta:
        ordering = ['deadline']
        verbose_name = "Work Package"
        verbose_name_plural = "Work Packages"

    def __str__(self):
        return f"{self.cpv_code} - {self.title}"
