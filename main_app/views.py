from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    """
    home view
    http://localhost:8000/
    """
    return render(request, 'home.html')

def about(request):
  """
  about view
  http://localhost/8000/about/
  """
  return render(request, 'about.html')

def bookings(request):
  """
  about view
  http://localhost/8000/bookings/
  """
  return render(request, 'bookings.html')

def equipment(request):
  """
  about view
  http://localhost/8000/equipment/
  """
  return render(request, 'equipment.html')

def portfolio(request):
  """
  about view
  http://localhost/8000/portfolio/
  """
  return render(request, 'portfolio.html')

def transactions(request):
  """
  about view
  http://localhost/8000/transactions/
  """
  return render(request, 'transactions.html')

def profile(request):
  """
  about view
  http://localhost/8000/profile/
  """
  return render(request, 'profile.html')


