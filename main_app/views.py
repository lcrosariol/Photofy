from ast import Del
from distutils.log import Log
import os
import uuid
import boto3
from datetime import date
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Equipment, Booking, Photo, Transaction
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  user = User.objects.all()
  return render(request, 'about.html')
  
def user_index(request):
  user = User.objects.all()
  return render(request, 'user/index.html', { 'user': user })

def user_detail(request):
  try:
    user = User.objects.get(id=user_id)
    equipments_user_doesnt_have = Equipment.objects.exclude(id__in = user.equipments.all().values_list('id'))
    return render(request, 'user/detail',{
      'user': user,
      'equipments': equipments_user_doesnt_have,
    })
  except User.DoesNotExist:
    return render(request, 'notfound.html')

def user_index(request):
  user = User.objects.all()
  return render(request, 'user/index.html', { 'user': user })



@login_required
def add_photo(request, user_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for s3 (filename)
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, user_id=user_id)
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', user_id=user_id)



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
      return redirect('index')
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



def assoc_equipment(request, user_id, equipment_id):
  """
  about view
  http://localhost/8000/equipment/
  """
  # equipment = Equipment.objects.filter(user=request.user)
  # return render(request, 'equipment.html', {'equipment': equipment})
  User.objects.get(id=user.id).equipments.add(equipment_id)
  return redirect('equipment', equipment_id=equipment_id)


def unassoc_equipment(request, user_id, equipment_id):
  User.objects.get(id=equipment_id).equipments.remove(equipment_id)
  return redirect('equipment', user_id=user_id)

class EquipmentList(ListView):
  model = Equipment


class EquipmentDetail(DetailView):
  model = Equipment


class EquipmentCreate(CreateView):
  model = Equipment
  fields = '__all__'


class EquipmentUpdate(UpdateView):
  model = Equipment
  fields = ['name', 'type']


class EquipmentDelete(DeleteView):
  model = Equipment
  success_url = '/'

@login_required
def portfolio(request):
  """
  about view
  http://localhost/8000/portfolio/
  """
  photos = Photo.objects.filter(user=request.user)
  print(user)
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

  
class TransactionCreate(LoginRequiredMixin, CreateView):
  model = Transaction
  fields = '__all__'


class TransactionUpdate(LoginRequiredMixin, UpdateView):
  model = Transaction
  fields = ['comment', 'booking']


class TransactionDelete(LoginRequiredMixin, DeleteView):
  model = Transaction
  success_url = '/transactions/'