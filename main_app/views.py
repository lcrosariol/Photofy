from ast import Del
from distutils.log import Log
import os
from re import L
import uuid
import boto3
from datetime import date
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Equipment, Booking, Photo, Transaction, Profile, User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
# Create your views here.


@login_required
def add_photo(request, photographer_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for s3 (filename)
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, user_id=photographer_id, name=key)
        except:
            print('An error occurred uploading file to S3')
    return redirect('portfolio')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('bookings')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def home(request):
    """
    home view
    http://localhost:8000/
    """
    return render(request, 'home.html')


def photographers(request):
    """
    photographers view
    http://localhost/8000/photographers/
    """
    # profiles = Profile.objects.all()

    users = User.objects.all()
    print("---------",users[0].profile.id)
    return render(request, 'photographers.html', {'users': users})


@login_required
def bookings(request):
    """
    http://localhost/8000/bookings/
    """
    today = date.today()
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/index.html', {'bookings': bookings, 'today': today})


@login_required
def equipment(request):
    """
    http://localhost/8000/equipment/
    """

    equipments = Equipment.objects.all()
    # profile = Profile.objects.get(user=request.user)
    # print(profile)
    print(equipments)
    return render(request, 'equipment.html', {'equipments': equipments})



def portfolio(request, profile_id):
    """
    http://localhost/8000/portfolio/
    """
    
    photos = Photo.objects.filter(user=profile_id)
    return render(request, 'portfolio.html', {'photos': photos})


@login_required
def booking(request, booking_id):
    """
    single booking view
    http://localhost/8000/portfolio/
    """
    today = date.today()
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'bookings/booking_detail.html', {'booking': booking, 'today': today})


@login_required
def transactions(request):
    """
    transactions view
    http://localhost/8000/transactions/
    """
    bookings = Booking.objects.filter(user=request.user)
    bookings_list = list(bookings)
    transactions = Transaction.objects.filter(booking__in=bookings_list)
    return render(request, 'transactions.html', {'transactions': transactions})


@login_required
def profile(request):
    """
    http://localhost/8000/profile/
    """
    return render(request, 'profile.html')

@login_required
def assoc_equipment(request, equipment_id):
  print('!!!!_------!!!!-----THIS', request.user.profile.id, equipment_id)
  Profile(id=request.user.profile.id).equipments.add(equipment_id)
  return redirect('equipment')

@login_required
def unassoc_equipment(request, equipment_id):
  print('!!!!_------!!!!-----THIS', request.user.profile.id, equipment_id)
  Profile(id=request.user.profile.id).equipments.remove(equipment_id)
  return redirect('equipment')

class TransactionCreate(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = '__all__'


class TransactionUpdate(LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = ['amount', 'paid']
    success_url = '/transactions/'


class TransactionDelete(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = '/transactions/'


class EquipmentList(LoginRequiredMixin, ListView):
    model = Equipment


class EquipmentCreate(LoginRequiredMixin, CreateView):
    model = Equipment
    fields = '__all__'


class EquipmentUpdate(LoginRequiredMixin, UpdateView):
    model = Equipment
    fields = ['model']


class EquipmentDelete(LoginRequiredMixin, DeleteView):
    model = Equipment
    success_url = '/equipment/'


class BookingCreate(LoginRequiredMixin, CreateView):
    model = Booking
    # take user field out because it is being attached when they click on the form (lines 176-178)
    fields = ['date', 'location', 'customer_name', 'phone_number', 'comment']
    success_url = '/bookings/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookingUpdate(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = ['date', 'location', 'customer_name', 'phone_number', 'comment']


class BookingDelete(LoginRequiredMixin, DeleteView):
    model = Booking
    success_url = '/bookings/'
