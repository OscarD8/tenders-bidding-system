from django.contrib import admin

from .models import Council, Project


class CouncilAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Council, CouncilAdmin)
admin.site.register(Project)
