from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, blank=True, verbose_name='Email')


class Test(models.Model):
    name = models.CharField(max_length=300, db_index=True, verbose_name='Название теста')
    subject = models.CharField(max_length=120, verbose_name='Тематика')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    def __str__(self):
        annotation = '{}: {}.'.format(self.subject, self.name)
        return annotation

    class Meta:
        db_table = 'test'
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class TestQuestions(models.Model):
    ANSWER_STATUS = [
        ('right', 'Верный'),
        ('wrong', 'Неправильный'),
    ]
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField(default=None, verbose_name='Вопрос')


class TestAnswers(models.Model):
    question = models.ForeignKey(TestQuestions, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField(default=None, verbose_name='Ответ')
    status = models.CharField(max_length=5, verbose_name='Правильный/неправильный')
