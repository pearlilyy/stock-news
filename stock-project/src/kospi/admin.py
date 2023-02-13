from django.contrib import admin

from .models import Company

# to search function


class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['company']


admin.site.register(Company, CompanyAdmin)
