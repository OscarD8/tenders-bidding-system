from django.contrib import admin

from .models import Council, Project, Requirement


admin.site.register(Council)
admin.site.register(Project)
admin.site.register(Requirement)