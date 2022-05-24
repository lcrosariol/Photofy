from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

EQUIPMENT_TYPE = (
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


class Equipment(models.Model):
    type = models.CharField(
        'Equipment Type',
        max_length=1,
        choices=EQUIPMENT_TYPE,
        default=EQUIPMENT_TYPE[0][0]
    )
    model = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.type} {self.model}'
        
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.id})

class Profile(User):
    equipment = models.ManyToManyField(Equipment)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.id}) 

class Photo(models.Model):
    url = models.URLField(max_length=350)
    description = models.TextField(blank=True)
    # on_delete refers to User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description}"


class Booking(models.Model):
    date = models.DateField('Booking Date')
    location = models.CharField(max_length=200)
    paid = models.BooleanField('Paid')
    customer_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.location} on {self.date}"

    class Meta:
        ordering = ['-date']


class Transaction(models.Model):
    payment_method = models.CharField(
        'Payment Method',
        max_length=1,
        choices=PAYMENT_TYPE,
        default=PAYMENT_TYPE[0][0]
    )
    amount = models.DecimalField('Amount',max_digits=12, decimal_places=2, default=0.0)
    date = models.DateField('Transaction Date')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.get_payment_method_display()} Payment on {self.date}"
