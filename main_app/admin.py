from django.contrib import admin

# Register your models here.
from .models import Equipment, Booking, Photo, Transaction, Profile

admin.site.register(Equipment)
admin.site.register(Booking)
admin.site.register(Transaction)
admin.site.register(Photo)
admin.site.register(Profile)