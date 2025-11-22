from django.contrib import admin

from .models import Council


class CouncilAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Council, CouncilAdmin)
