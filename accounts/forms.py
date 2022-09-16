from allauth.account.forms import SignupForm
from django.forms import CharField, EmailField, EmailInput, HiddenInput, ModelForm, TextInput
from django.forms.widgets import Input, Textarea
from django.contrib.auth import get_user_model
from .models import Message, ResponseMessage

User = get_user_model()


class SimpleSignupForm(SignupForm):
    phone = CharField(max_length=11, label='Phone:')
    first_name = CharField(max_length=255, label='First Name:')
    last_name = CharField(max_length=255, label='Last Name:')

    def save(self, request):
        user = super(SimpleSignupForm, self).save(request)
        user.phone = self.cleaned_data['phone']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class EditProfileForm(ModelForm):
    phone = CharField(max_length=11, label='Phone:', widget=Input(
        attrs={
            'class': 'form-control',
            'required': True,
        }
    ))
    first_name = CharField(max_length=255, label='First name:', widget=Input(
        attrs={
            'class': 'form-control',
            'required': True,
        }
    ))
    last_name = CharField(max_length=255, label='Last name:', widget=Input(
        attrs={
            'class': 'form-control',
            'required': True,
        }
    ))
    address = CharField(label='Address:', widget=TextInput(
        attrs={
            'class': 'form-control',
            'required': True,
        }
    ))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'address']


class MessageForm(ModelForm):
    subject = CharField(max_length=255, required=True, widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Subject'
    }))

    message = CharField(required=True, widget=Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Message'
    }))

    class Meta:
        model = Message
        fields = ['subject', 'message']


class ResponseMessageForm(ModelForm):
    subject = CharField(max_length=255, required=True, widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Subject'
    }))

    message = CharField(required=True, widget=Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Message'
    }))

    class Meta:
        model = ResponseMessage
        fields = ['subject', 'message']


class ResponseMessageFormTwo(ResponseMessageForm):
    receiver = CharField(max_length=255, required=True, widget=HiddenInput(attrs={
        'class': 'form-control',
        'placeholder': 'Subject',

    }))
