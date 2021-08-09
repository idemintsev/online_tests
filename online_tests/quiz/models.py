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
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='question', verbose_name='Название теста')
    text = models.TextField(default='', verbose_name='Вопрос')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text if len(str(self.text)) < 20 else f'{str(self.text[:20])}...'


class Answer(models.Model):
    STATUS = [
        ('right', 'Правильный'),
        ('wrong', 'Неправильный'),
    ]
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer', verbose_name='Вопрос')
    text = models.TextField(default='', verbose_name='Ответ')
    status = models.CharField(max_length=12, choices=STATUS, verbose_name='Правильный/Неправильный')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.text if len(str(self.text)) < 20 else f'{str(self.text[:20])}...'


class UserQuizResults(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Название теста')
    right_answers_quantity = models.IntegerField(default=0, blank=True, verbose_name='Количество правильных ответов')
    wrong_answers_quantity = models.IntegerField(default=0, blank=True, verbose_name='Количество неправильных ответов')
