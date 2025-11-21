from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'price', 'location', 'is_available', 'date_posted')
    list_filter = ('property_type', 'is_available')
    search_fields = ('title', 'location')
