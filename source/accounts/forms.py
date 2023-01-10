from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from accounts.models import Profile
from django import forms


class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2','first_name', 'last_name', 'email']
        field_classes = {'username': UsernameField}


    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if last_name or first_name:
            pass
        else:
            raise ValidationError('Fill out First name or Second name ')

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}

class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar','git_profile','about_user']

