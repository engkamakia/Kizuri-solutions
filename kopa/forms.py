from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    id_number = forms.CharField(max_length=20, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required.')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'id_number', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email