from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'password1', 'password2', 'email']
        field_classes = {'username': UsernameField}

    def clean(self):
        cleaned_data = super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        if len(first_name) == 0 and len(last_name) == 0:
            raise ValidationError('At least one of the name fields must be fill')
        elif len(email) == 0:
            raise ValidationError('Email field must be fill')
        else:
            return cleaned_data
