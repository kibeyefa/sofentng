from django.forms import CharField, FileField, Form
from django.forms.widgets import *
from django import forms
from .models import *



class DonateItemForm(forms.ModelForm):

  title = CharField(required=True, max_length=255, widget=TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Item name'
  }))

  description = CharField(required=True, max_length=255, widget=Textarea(attrs={
    'class': 'form-control',
  }))

  class Meta:
    model = DonateItem
    fields = ['title', 'description']



class DonateItemEditImagesForm(Form, DonateItemForm):

  images = FileField(required=False, allow_empty_file=True, widget=FileInput(attrs={
    'class': 'form-control',
    'multiple': True,
    'accept': 'images/png, images/jpeg, images/jpg'
  }))
