from django.contrib import admin

# Register your models here.
from .models import Equipment, Bookings, Photo, Transactions, Customer

admin.site.register(Equipment)
admin.site.register(Bookings)
admin.site.register(Transactions)
admin.site.register(Customer)