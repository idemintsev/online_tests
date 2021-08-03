from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(
        max_length=100,
        help_text='Обязательное поле. Не более 150 символов. Только английские буквы, цифры и символы @/./+/-/_.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
