from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.forms.models import BaseInlineFormSet


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        help_text='Обязательное поле. Не более 150 символов. Только английские буквы, цифры и символы @/./+/-/_.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AnswerInLineFormset(BaseInlineFormSet):
    def clean(self):
        for error in self.errors:
            if error:
                return

        # Проверяем, чтобы не все вопросы были правильными/неправильными
        answers_statuses = [answer.get('status') for answer in self.cleaned_data if answer]
        if 'right' not in answers_statuses or 'wrong' not in answers_statuses:
            raise ValidationError('Все ответы не могут быть правильными или неправильными')
