from django.db import models


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
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField(default=None, verbose_name='Вопрос')


class TestAnswers(models.Model):
    ANSWER_STATUS = [
        ('right', 'Верный'),
        ('wrong', 'Неправильный'),
    ]
    question = models.ForeignKey(TestQuestions, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField(default=None, verbose_name='Ответ')
    status = models.CharField(
        max_length=5, choices=ANSWER_STATUS, default='wrong', verbose_name='Правильный/неправильный'
    )
