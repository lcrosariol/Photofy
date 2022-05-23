from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

EQUIPMENT = (
  ('V', 'Video'),
  ('P', 'Photo'),
  ('O', 'Other')
)

PAYMENT_TYPE = (
    ('C', 'Card'),
    ('O', 'Online'),
    ('Z', 'Zelle'),
    ('X', 'Cash'),
)

# Create your models here.
class Equipment(models.Model):
    type = models.CharField(
    'Equipment Type',
    max_length=1,
    choices=EQUIPMENT,
    default=EQUIPMENT[0][0]
  )
    model = models.CharField(max_length=40)
    
    def __str__(self):
        return f'{self.type} {self.model}'


class Photo(models.Model):
    url = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) #on_delete refers to User model
    
    def __str__(self):
        return f"{self.description}"
    

class Bookings(models.Model):
    date = models.DateField('Booking Date')
    location = models.CharField(max_length=200)
    paid = models.BooleanField('Paid')
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.location} on {self.date}"
    
    class Meta:
        ordering = ['-date']
        

class Transactions(models.Model):
    payment_method = models.CharField(
        'Payment Method',
        max_length=1,
        choices=PAYMENT_TYPE,
        default=PAYMENT_TYPE[0][0]
        )
    amount = models.FloatField('Amount')
    date = models.DateField('Transaction Date')
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"{self.get_payment_method_display()} Payment on {self.date}"
