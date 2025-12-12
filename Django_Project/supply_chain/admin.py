from django.contrib import admin

from .models import Council, Project, Requirement, Bid

admin.site.register(Council)
admin.site.register(Project)
admin.site.register(Requirement)
admin.site.register(Bid)