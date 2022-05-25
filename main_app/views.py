from ast import Del
from distutils.log import Log
import os
import uuid
import boto3
from datetime import date
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Equipment, Booking, Photo, Transaction, Profile
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


@login_required
def add_photo(request, photographer_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for s3 (filename)
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
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


@login_required
def about(request):
  """
  about view
  http://localhost/8000/about/
  """
  return render(request, 'about.html')


@login_required
def bookings(request):
  """
  about view
  http://localhost/8000/bookings/
  """
  today = str(date.today())
  bookings = Booking.objects.filter(user=request.user)
  print(today)
  print(bookings)
  return render(request, 'bookings/index.html', {'bookings': bookings, 'date': today})


@login_required
def equipment(request):
  """
  about view
  http://localhost/8000/equipment/
  """
  
  equipments = Equipment.objects.all()
  # profile = Profile.objects.get(user=request.user)
  # print(profile)
  print(equipments)
  return render(request, 'equipment.html', {'equipments': equipments})


@login_required
def portfolio(request):
  """
  about view
  http://localhost/8000/portfolio/
  """
  photos = Photo.objects.filter(user=request.user.id)
  return render(request, 'portfolio.html', {'photos': photos})


@login_required
def booking(request, booking_id):
  """
  single booking view
  http://localhost/8000/portfolio/
  """
  booking = Booking.objects.get(id=booking_id)
  return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def transactions(request):
  """
  transactions view
  http://localhost/8000/transactions/
  """
  bookings = Booking.objects.filter(user=request.user)
  bookings_list = list(bookings)
  transactions = Transaction.objects.filter(booking__in = bookings_list )
  return render(request, 'transactions.html', {'transactions': transactions})


@login_required
def profile(request):
  """
  about view
  http://localhost/8000/profile/
  """
  return render(request, 'profile.html')


def assoc_equipment(request, equipment_id):
  Profile.objects.get(id=request.user.id).equipments.add(equipment_id)
  print('THIS', request.user.id, equipment_id)
  return redirect('equipment')

def unassoc_equipment(request, profile_id, equipment_id):
  Profile.objects.get(user_id=profile_id).equipment.remove(equipment_id)
  return redirect('equipment', profile_id=profile_id)

  
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
  #take user field out because it is being attached when they click on the form (lines 176-178)
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
