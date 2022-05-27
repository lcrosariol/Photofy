from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum


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
    """
    Profile can contain many Equipment. Related to :model:`main_app.Profile`

    **Views**

    Equipment - :view:`main_app.views.equipment`

    Associated Equipment - :view:`main_app.views.assoc_equipment`

    """
    type = models.CharField(
        'Equipment Type',
        max_length=1,
        choices=EQUIPMENT_TYPE,
        default=EQUIPMENT_TYPE[0][0]
    )
    model = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.get_type_display()} {self.model}"
    
    def get_absolute_url(self):
        return reverse('equipment')


class Profile(models.Model):
    """
    User model extended by making Profile model. Related to :model:`auth.User`
    Extended to have many to many relationship with :model:`main_app.Equipment`
    
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    equipments = models.ManyToManyField(Equipment, blank=True)
    
    name = models.CharField(max_length=40, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    facebook = models.URLField(max_length = 250, null=True, blank=True)
    linkedin = models.URLField(max_length = 250, null=True, blank=True)
    instagram = models.URLField(max_length = 250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
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
    """
    Photo belongs to the user and the user can upload many photos to their portfolio.
    Related to :model:`auth.User`

    **Views**

    Portfolio - :view:`main_app.views.portfolio`

    Add Photo - :view:`main_app.views.add_photo`

    """
    url = models.URLField(max_length=350)
    description = models.TextField(blank=True, null=True)
    # on_delete refers to User model
    name = models.CharField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name}"


class Booking(models.Model):
    """
    User can have many Bookings. Represents the booking between photographer(user) and the customer(customer_name).
    Related to :model:`auth.User`

    **Views**

    All Bookings - :view:`main_app.views.bookings`

    View Booking - :view:`main_app.views.booking`

    """
    date = models.DateField('Booking Date')
    location = models.CharField(max_length=200)
    customer_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    
    def __str__(self):
        return f"{self.date} -- {self.customer_name} at {self.location}"

    class Meta:
        ordering = ['-date']
    
    def get_absolute_url(self):
        return reverse('booking', kwargs={'booking_id': self.id})


class Transaction(models.Model):
    """
    Transaction represents the transaction between photographer and customer.

    One to one relationship with :model:`main_app.Booking`

    **Views**

    View Transactions :view:`main_app.views.transactions`

    Part of Booking in :view:`main_app.views.booking`

    """
    payment_method = models.CharField(
        'Payment Method',
        max_length=1,
        choices=PAYMENT_TYPE,
        default=PAYMENT_TYPE[0][0]
    )
    amount = models.DecimalField('Amount',max_digits=12, decimal_places=2, default=0.0)
    date = models.DateField('Transaction Date')
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    paid = models.BooleanField('Paid')

    def __str__(self):
        return f"{self.get_payment_method_display()} Payment of ${self.amount} on {self.date} for {self.booking}"

    def get_absolute_url(self):
        return reverse('transactions')
    
    