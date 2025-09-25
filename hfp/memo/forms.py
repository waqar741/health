from django import forms
from .models import Memo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields =['text','photo']

class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')