import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Equipment, Bookings, Photo, Transactions, Customer
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def home(request):
  return HttpResponse('<h1>HELLOOOO</h1>')