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

    # --- BAMBOO STANDARD EXTENSION ---
    class BambooStandard(models.TextChoices):
        GOING_GREEN = 'GREEN', 'Going Green'
        ECO_AWARE = 'AWARE', 'Eco-Conscious'
        CLIMATE_LEADER = 'LEADER', 'Climate Leader'
        REGENERATIVE = 'REGEN', 'Regenerative Pioneer'

    bamboo_standard = models.CharField(
        max_length=10,
        choices=BambooStandard.choices,
        default=BambooStandard.GOING_GREEN,
        help_text="The sustainability rating of this council within the network."
    )

    # --- REGION EXTENSION ---
    class Region(models.TextChoices):
        NORTH_EAST = 'NE', 'North East'
        NORTH_WEST = 'NW', 'North West'
        YORKSHIRE = 'YH', 'Yorkshire and the Humber'
        EAST_MIDLANDS = 'EM', 'East Midlands'
        WEST_MIDLANDS = 'WM', 'West Midlands'
        EAST_ENGLAND = 'EE', 'East of England'
        LONDON = 'LDN', 'London'
        SOUTH_EAST = 'SE', 'South East'
        SOUTH_WEST = 'SW', 'South West'
        SCOTLAND = 'SCT', 'Scotland'
        WALES = 'WLS', 'Wales'

    region = models.CharField(
        max_length=5,
        choices=Region.choices,
        default=Region.YORKSHIRE
    )

    # --- MISSION EXTENSION ---
    sustainability_mission = models.TextField(
        blank=True,
        default="Committed to reducing carbon emissions and promoting circular economy principles in all local infrastructure projects.",
        help_text="The council's key sustainability quote or mission statement."
    )

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

    # --- SUSTAINABILITY GOAL EXTENSION ---
    sustainability_goal = models.TextField(
        blank=True,
        help_text="Describe the specific ecological impact metrics (e.g., 'Reduces carbon by 40%...').",
        default="This project aims to significantly reduce local carbon emissions and improve biodiversity."
    )

    # --- FUNDING SOURCE EXTENSION ---
    class FundingSource(models.TextChoices):
        UK_GREEN_LEVY = 'LEVY', 'UK Green Levy'
        DIRECT_GRANT = 'GRANT', 'Direct Council Grant'
        PRIVATE_PARTNERSHIP = 'PPP', 'Private-Public Partnership'
        LOTTERY_FUND = 'LOTTERY', 'National Lottery Heritage Fund'
        RESILIENCE_FUND = 'RESILIENCE', 'Climate Resilience Fund'

    funding_source = models.CharField(
        max_length=20,
        choices=FundingSource.choices,
        default=FundingSource.UK_GREEN_LEVY,
        verbose_name="Funding Source"
    )

    # --- MANDATE EXTENSION ---
    class Mandate(models.TextChoices):
        NET_ZERO_2030 = 'NZ30', 'Net Zero 2030'
        BIODIVERSITY_2025 = 'BIO25', 'Biodiversity Gain 2025'
        CLEAN_AIR = 'AIR', 'Clean Air Zone (CAZ)'
        HOUSING_STD = 'FHS', 'Future Homes Standard'

    policy_mandate = models.CharField(
        max_length=20,
        choices=Mandate.choices,
        default=Mandate.NET_ZERO_2030,
        verbose_name="Policy Mandate"
    )

    objects = ProjectManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Projects"

    def __str__(self):
        return f'{self.title}'

    @property  # Treat this function like a variable. Don't make me use brackets () to call it.
    def percentage_allocated(self):  # this is like an interface
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
