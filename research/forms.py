from django.forms import *
from django.forms.fields import *
from .models import *


class ResearchAddForm(ModelForm):
  name = CharField(required=True, widget=TextInput(attrs={
    'class': 'form-control'
  }))
  file = FileField(required=True, widget=FileInput(attrs={
    'class': 'form-control',
  }))
  
  class Meta:
    model = ResearchDocument
    fields = ['name', 'file']

  def save(self, *args, **kwargs):
    return super().save(*args, **kwargs)