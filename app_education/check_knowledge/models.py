from django.contrib.auth.models import User
from django.db import models
from django.db import connection


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

    def get_answers(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT answer, status
                FROM check_knowledge_testanswers
                WHERE question_id = %s""", [self.id])
            result = cursor.fetchone()
        return result


class TestQuestions(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField(default=None, verbose_name='Вопрос')

    def __str__(self):
        return self.question

    def get_answers(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT answer, status
                FROM check_knowledge_testanswers
                WHERE question_id = %s""", [self.id])
            result = cursor.fetchone()
        return result


class TestAnswers(models.Model):
    ANSWER_STATUS = [
        ('right', 'Верный'),
        ('wrong', 'Неправильный'),
    ]
    question = models.ForeignKey(TestQuestions, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField(default=None, verbose_name='Ответ')
    status = models.CharField(max_length=5, choices=ANSWER_STATUS, verbose_name='Правильный/неправильный')

    def __str__(self):
        return self.answer
