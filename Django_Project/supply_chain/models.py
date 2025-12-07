from django.core.validators import RegexValidator
from django.db import models


class Council(models.Model):
    name = models.CharField(max_length=100)

    contact = models.CharField(max_length=100)
    contact_email = models.EmailField()

    slug = models.SlugField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Councils"
        ordering = ['name']

    def __str__(self):
        return f'{self.name} Council'


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    budget = models.IntegerField()

    council = models.ForeignKey(Council, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Projects"

    def __str__(self):
        return f'{self.title}'


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
