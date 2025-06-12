from django.contrib import admin
from vendor.models import vendor
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ('user','vendor_name', 'is_approved','created_at','vendor_license')
    lsit_display_links = ('user','vendor_name')
admin.site.register(vendor,VendorAdmin)