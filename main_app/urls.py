"""photofy URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Main page routes
    path('', views.bookings, name='bookings'),
    path('accounts/signup/', views.signup, name='signup'),
    # Bookings routes
    path('bookings/', views.bookings, name='bookings'),
    path('bookings/create/', views.BookingCreate.as_view(), name='booking_create'),
    path('bookings/<int:pk>/update/', views.BookingUpdate.as_view(), name='booking_update'),
    path('bookings/<int:pk>/delete/', views.BookingDelete.as_view(), name='booking_delete'),
    path('bookings/<int:booking_id>', views.booking, name='booking'),

    # Equipments routes
    path('equipment/', views.equipment, name='equipment'),
    path('equipment/create/', views.EquipmentCreate.as_view(), name='equipment_create'),
    path('equipment/<int:pk>/update/', views.EquipmentUpdate.as_view(), name='equipment_update'),
    path('equipment/<int:pk>/delete/', views.EquipmentDelete.as_view(), name='equipment_delete'),
    path('equipment/assoc_equipment/<int:equipment_id>/', views.assoc_equipment, name='assoc_equipment'),
    path('equipment/unassoc_equipment/<int:equipment_id>/', views.unassoc_equipment, name='unassoc_equipment'),
    # Portfolio routes
    path('portfolio/<int:profile_id>', views.portfolio, name='portfolio'),
    path('portfolio/<int:photographer_id>/add_photo/', views.add_photo, name='add_photo'),
    # Photographers route
    path('photographers/', views.photographers, name='photographers'),
    # Transactions routes
    path('transactions/', views.transactions, name='transactions'),
    path('transaction/create/', views.TransactionCreate.as_view(), name='transaction_create'),
    path('transaction/<int:pk>/update/', views.TransactionUpdate.as_view(), name='transaction_update'),
    path('transaction/<int:pk>/delete/', views.TransactionDelete.as_view(), name='transaction_delete'),
    # Profile route
    path('profile/<int:pk>/', views.ProfileUpdate.as_view(), name='profile'),
]
