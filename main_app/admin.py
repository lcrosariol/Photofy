from django.contrib import admin

# Register your models here.
from .models import Equipment, Booking, Photo, Transaction

admin.site.register(Equipment)
admin.site.register(Booking)
admin.site.register(Transaction)
