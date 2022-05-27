import os
from re import L
import uuid
import boto3
from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Equipment, Booking, Photo, Transaction, Profile, User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import EquipmentForm
# Create your views here.


@login_required
def add_photo(request, photographer_id):
    """
    Function to upload photo from user to AWS S3 Bucket.

    ``Models Related``

    Photo: :model:`main_app.Photo`

    User: :model:`auth.User`

    """
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
    return HttpResponseRedirect(f'/portfolio/{photographer_id}')

def signup(request):
    """
    User sign up page

    **Template**

    :template:`main_app/registration/signupm.html`

    **URL**

    http://localhost:8000/accounts/signup/
    
    """
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
    **Template**

    :template:`main_app/home.html`

    **URL**

    http://localhost:8000/

    """
    return render(request, 'home.html')


def photographers(request):
    """
    Displays all photographers on application. 

    ``Models Related``

    User: :model:`auth.User`

    **Template**

    :template:`main_app/photographers.html`

    **URL**

    http://localhost/8000/photographers/

    """
    users = User.objects.all()
    return render(request, 'photographers.html', {'users': users})


@login_required
def bookings(request):
    """
    Displays all bookings for current user

    ``Models Related``

    Booking: :model:`main_app.Booking`

    **Template**

    :template:`main_app/bookings/index.html`

    **URL**

    http://localhost/8000/bookings/

    """
    today = date.today()
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/index.html', {'bookings': bookings, 'today': today})


@login_required
def equipment(request):
    """
    Displays all equipment the user does and does not have

    ``Models Related``

    Equipment: :model:`main_app.Equipment`

    **Template**

    :template:`main_app/equipment.html`

    **URL**
    http://localhost/8000/equipment/

    """
    assoc_equipments = Equipment.objects.filter(profile=request.user.profile.id)
    gear_user_doesnt_have = Equipment.objects.exclude(id__in = assoc_equipments.all().values_list('id'))
    return render(request, 'equipment.html',  {'equipments': gear_user_doesnt_have, 'assoc_equipments': assoc_equipments})



def portfolio(request, profile_id):
    """
    Displays all photos belonging to photographer

    ``Models Related``

    Photo :model:`main_app.Photo`

    **Template**

    :template:`main_app/portfolio.html`

    http://localhost/8000/portfolio/

    """
    profile_user = User.objects.get(id=profile_id)
    photos = Photo.objects.filter(user=profile_id).order_by('-created_at')
    return render(request, 'portfolio.html', {'photos': photos, 'profile_id': profile_id, "profile_user":profile_user})


@login_required
def booking(request, booking_id):
    """
    Displays single booking belonging to photographer

    ``Models Related``

    Booking: :model:`main_app.Booking`

    **Template**

    :template:`main_app/bookings/booking_detail.html`

    *URL*

    http://localhost/8000/portfolio/

    """
    today = date.today()
    booking = Booking.objects.get(id=booking_id)

    try:
        booking.transaction
        no_transaction = True
        return render(request, 'bookings/booking_detail.html', {'booking': booking, 'today': today, 'no_transaction': no_transaction})
    except:
        no_transaction = False
        return render(request, 'bookings/booking_detail.html', {'booking': booking, 'today': today, 'no_transaction': no_transaction})


@login_required
def transactions(request):
    """
    Displays transactions made by photographer

    ``Models Related``

    Transaction: :model:`main_app.Transaction`
    
    Booking: :model:`main_app.Booking`

    **Template**

    :template:`main_app/transactions.html`

    **URL**

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
  Profile(id=request.user.profile.id).equipments.add(equipment_id)
  return redirect('equipment')

@login_required
def unassoc_equipment(request, equipment_id):
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
    form_class = EquipmentForm
    success_url = '/equipment/'



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

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['email', 'facebook', 'linkedin', 'twitter', 'instagram']
    success_url = '/photographers/' 