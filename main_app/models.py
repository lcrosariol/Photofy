from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

EQUIPMENT = (
  ('V', 'Video'),
  ('P', 'Photo'),
  ('O', 'Other')
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
    user = models.ForeignKey(User, on_delete=models.CASCADE) #on_delete refers to User model
    
    def __str__(self):
        return f"Favorite Photo: {self.cat.id} @ {self.url}"