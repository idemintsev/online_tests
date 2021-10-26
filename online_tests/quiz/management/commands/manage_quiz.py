from django.core.management.base import BaseCommand

from quiz.models import Quiz, Question, Answer


class Command(BaseCommand):
    help = 'Позволяет создать или удалить из БД тестовый набор викторин'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            type=str,
            help='create - создать викторины, delete - удалить викторины'
        )

    def handle(self, *args, **kwargs):
        action = kwargs['action']

        if action == 'create':
            self.create_quiz()
        elif action == 'delete':
            self.delete_quiz()
        else:
            self.stdout.write('Переданы некорректные аргументы. Необходимо указать либо create, либо delete')

    def create_quiz(self):
        quiz = Quiz.objects.create(name='Тестовая викторина', subject='Тестовая тема')

        for question_number in range(1, 3):
            self.create_questions_and_answers(quiz, question_number)

        self.stdout.write('Данные добавлены')

    def create_questions_and_answers(self, quiz, question_number):
        question = Question.objects.create(text=f'Тестовый вопрос №{question_number}', quiz=quiz)
        self.create_answers(question)

    def create_answers(self, question):
        Answer.objects.bulk_create([
            Answer(question=question, text='Правильный ответ', status='right'),
            Answer(question=question, text='Первый неправильный ответ', status='wrong'),
            Answer(question=question, text='Второй неправильный ответ', status='wrong'),
        ])

    def delete_quiz(self):
        is_exist = Quiz.objects.filter(name='Тестовая викторина').exists()
        if is_exist:
            Quiz.objects.filter(name='Тестовая викторина').delete()
            self.stdout.write('Данные удалены')
