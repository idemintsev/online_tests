from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Quiz(models.Model):
    name = models.CharField(max_length=300, verbose_name='Название')
    subject = models.CharField(max_length=120, verbose_name='Тематика')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    class Meta:
        verbose_name = 'Тесты'
        verbose_name_plural = 'Тесты'
        ordering = ['-created_date', 'subject']

    def __str__(self):
        return f'"{self.name}" ({self.subject})'

    def get_absolute_url(self):
        return reverse('quiz', kwargs={'pk': self.pk})


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Название теста')
    text = models.TextField(default='', verbose_name='Вопрос')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text if len(str(self.text)) < 20 else self.text[:20]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, blank=True, verbose_name='Email')

