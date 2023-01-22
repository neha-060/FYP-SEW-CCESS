from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
# admin.site.register(CustomerProfile)
# admin.site.register(CustomerManager)
admin.site.register(Tailor)
# admin.site.register(TailorProfile)
# admin.site.register(TailorManager)
# admin.site.register(Cart)
admin.site.register(Service)
admin.site.register(Shipper)
admin.site.register(Order)
admin.site.register(Clothe)
admin.site.register(BillingInfo)
admin.site.register(Extra)
admin.site.register(Pickup)