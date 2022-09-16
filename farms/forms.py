from django.forms import *
from django.forms.fields import *
from .models import *


class ProduceForm(ModelForm):
  name = CharField(required=True, widget=TextInput(attrs={
    'class': 'form-control'
  }))
  price_per_unit = IntegerField(required=True, widget=NumberInput(attrs={
    'class': 'form-control'
  }))

  unit_name = CharField(required=True, widget=TextInput(attrs={
    'class': 'form-control'
  }))

  class Meta:
    model = FarmProduce
    fields = ['name', 'price_per_unit', 'unit_name']