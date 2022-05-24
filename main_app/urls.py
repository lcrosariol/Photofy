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

    path('', views.home, name='home'),

    # #home page
    path('about/', views.about, name='about'),
    # #about page
    path('bookings/', views.bookings, name='bookings'),
    
    # #bookings page
    path('bookings/<int:booking_id>', views.booking, name='booking'),

    path('equipment/', views.equipment, name='equipment'),
    #equiptment page
    path('portfolio/', views.portfolio, name='portfolio'),
    #portfolio page

    path('portfolio/<int:photographer_id>/add_photo/', views.add_photo, name='add_photo'),
    #add photographer_id to photo and function will tell it to add to the portfolio, and redirect to portfolio

    path('transactions/', views.transactions, name='transactions'),
    #transactions page

    path('transaction/create/', views.TransactionCreate.as_view(), name='transaction_create'),
    path('transaction/<int:pk>/update/', views.TransactionUpdate.as_view(), name='transaction_update'),
    path('transaction/<int:pk>/delete/', views.TransactionDelete.as_view(), name='transaction_delete'),

    path('profile/', views.profile, name='profile'),
    #user profile page

    path('accounts/signup/', views.signup, name='signup'),




]
