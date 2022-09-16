from dataclasses import fields
from django import forms
from django.forms.fields import *
from django.forms.widgets import *

from .models import *
from .models import ShopItemReview



PAYMENT_CHOICES = (
  ('c', "Credit card"), 
  ('d', "Pay on delivery")
)

class CheckOutForm(forms.Form):
  first_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
    'class': 'form-control'
  }))
  last_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
    'class': 'form-control'
  }))
  email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
    'class': 'form-control'
  }))
  phone = forms.CharField(max_length=11,required=True, widget=forms.TextInput(attrs={
    'class': 'form-control'
  }))
  address = forms.CharField(required=True, widget=forms.Textarea(attrs={
    'class': 'form-control'
  }))
  update_profile = forms.BooleanField(label="Use details to update my profile", required=False, widget=forms.CheckboxInput(attrs={
    'class': 'form-check-input'
  }))
  payment_options = forms.ChoiceField(required=True, choices=PAYMENT_CHOICES ,widget=forms.RadioSelect(attrs={
    'class': 'form-check-input',
  }))
  # address = 
  # email = 


class ShopItemReviewForm(forms.ModelForm):

  class Meta:
    model = ShopItemReview
    fields = ['subject', 'stars', 'review']



class SaleCreationForm(forms.ModelForm):

  class Meta:
    model = Sale
    fields = ['price', 'quantity']
