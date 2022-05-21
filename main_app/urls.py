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
    #home page
    path('bookings/', views.bookings, name='bookings'),
    #bookings page






    
    path('customer/', views.CustomerList.as.view(), name='customer_index'),
    #customer page
    path('customer/<intA:pk>/', views.CustomerDetail.as_view(), name='customer_detail'),
    #view customer detail
    path('customer/create/', views.CustomerCreate, name='customer_create'),
    #create a new customer
    path('customer/<int:pk>/update/', views.CustomerUpdate.as_view(), name='customer_update'),
    #update a customer
    path('customer/<int:pk>/delete/', views.CustomerDelete.as_view(), name='customer_delete'),
    #delete a customer
    path('equiptment/', views.equiptment, name='equiptment'),
    #equiptment page
    path('portfolio/', views.portfolio, name='portfolio'),
    #portfolio page
    path('transactions/', views.transactions, name='transactions'),
    #list of transactions may be seperate page or added to customer page...
    path('profile/', views.profile, name='profile'),
    #user profile page

]
