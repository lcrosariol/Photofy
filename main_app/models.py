from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
        return reverse('equipment')



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    equipments = models.ManyToManyField(Equipment, blank=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Photo(models.Model):
    url = models.URLField(max_length=350)
    description = models.TextField(blank=True, null=True)
    # on_delete refers to User model
    name = models.CharField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name}"


class Booking(models.Model):
    date = models.DateField('Booking Date')
    location = models.CharField(max_length=200)
    customer_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.location} on {self.date}"

    class Meta:
        ordering = ['-date']
    
    def get_absolute_url(self):
        return reverse('bookings')


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
    paid = models.BooleanField('Paid')

    
    def __str__(self):
        return f"{self.get_payment_method_display()} Payment on {self.date}"
