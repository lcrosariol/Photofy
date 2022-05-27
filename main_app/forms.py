from django.forms import ModelForm
from .models import Equipment
from django import forms

class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = ['type', 'model']

