from ast import Del
from distutils.log import Log
import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Equipment, Booking, Photo, Transaction
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
      Photo.objects.create(url=url, photographer_id=photographer_id)
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', photographer_id=photographer_id)



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
  bookings = Booking.objects.filter(user=request.user)
  return render(request, 'bookings.html', {'bookings': bookings})


@login_required
def equipment(request):
  """
  about view
  http://localhost/8000/equipment/
  """
  equipment = Equipment.objects.filter(user=request.user)
  return render(request, 'equipment.html', {'equipment': equipment})



@login_required
def portfolio(request):
  """
  about view
  http://localhost/8000/portfolio/
  """
  return render(request, 'portfolio.html')

@login_required
def transactions(request):
  """
  transactions view
  http://localhost/8000/transactions/
  """
  return render(request, 'transactions.html')


##do we want to create a transaction folder and add these to it?
@login_required
def transaction_detail(request):
  """
  transaction detail view
  http://localhost/8000/transactions/transactions_id
  """
  return render(request, 'transactions/detail.html')

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