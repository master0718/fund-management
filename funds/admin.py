from django.contrib import admin
from .models import Fund

@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ['name', 'strategy', 'aum', 'inception_date']
    list_filter = ['strategy']
    search_fields = ['name']
