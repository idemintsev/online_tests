from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from quiz.forms import UserRegisterForm
from quiz.models import Quiz, Question, Answer, UserQuizResults

MENU = [{'title': 'Главная', 'url_name': 'index'},
        {'title': 'О проекте', 'url_name': 'about'},
        {'title': 'Предложить тест', 'url_name': 'offer'}, ]


class IndexView(ListView):
    model = Quiz
    template_name = 'quiz/index.html'
    context_object_name = 'quizzes_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = MENU
        return context


class QuizView(View):
    def get(self, request, pk):
        quiz = Quiz.objects.get(id=pk)
        return render(request, 'quiz/quiz.html', {'quiz': quiz, 'menu': MENU})


class QuizPassingView(LoginRequiredMixin, View):
    redirect_field_name = 'index'

    def get(self, request):
        """
        quiz_pk - PK конкретного теста.
        Передается в шаблоне через URL от страницы к странице. По нему достаются вопросы из БД для конкретного теста.
        questions_id - кортеж из PK вопросов к тесту.
        По questions_id фильтруются варианты ответов.
        """
        quiz_pk = request.GET.get('quiz_pk')
        questions_queryset = Question.objects.filter(quiz_id=quiz_pk)  # вопросы для текущего теста
        if self.is_questions_for_quiz(questions_queryset):
            context = self.add_pagination(request, questions_queryset)
            questions_id = self.get_questions_id(questions_queryset)
            answers = self.get_answers_from_db(questions_id)
            # получаем номер индекса нужного кортежа с объектами Answer в answers.
            # answers[0] - кортеж с объектами Answer на 1-й вопрос, answers[1] - 2-й вопрос и т.д.
            answers_index_for_current_question = 0 if context['page'] is None else (int(context['page']) - 1)
            answers = answers[answers_index_for_current_question]
            context.update(quiz_pk=quiz_pk, answers=answers)
            context['menu'] = MENU
            return render(request, 'quiz/passing.html', context)
        return render(request, 'quiz/passing.html')

    def post(self, request):
        data = request.POST.getlist('input')
        page, quiz_pk, question_pk = self.get_page_quiz_id_question_id(data)
        right_answers = self.get_right_answers(question_pk)
        user_answers = self.get_user_answers_from_templates(data)
        self.answer_handler(
            right_answers=right_answers,
            user_answers=user_answers,
            user=request.user,
            quiz=Quiz.objects.get(id=quiz_pk),
        )
        questions_queryset = Question.objects.filter(quiz_id=quiz_pk)  # вопросы для текущего теста
        context = self.add_pagination(request, questions_queryset, page)
        context.update(quiz_pk=quiz_pk, message='Ваш ответ приинят')
        return render(request, 'quiz/passing.html', context)

    def is_questions_for_quiz(self, questions_queryset):
        """ Проверяет есть ли вопросы для теста """
        if len(questions_queryset):
            return True
        return False

    def get_right_answers(self, question_id) -> list:
        """ Возвращает список правильных ответов для конкретного вопроса в тесте. """
        right_answers_queryset = Answer.objects.filter(question=question_id, status='right')
        right_answers_list = [answer.id for answer in right_answers_queryset]
        return right_answers_list

    def get_user_answers_from_templates(self, data_from_templates):
        all_data = [data.split(',') for data in data_from_templates]
        user_answers = [int(answer[-1]) for answer in all_data]
        return user_answers

    def is_right_answer(self, right_answers: list, user_answers: list) -> bool:
        """ Проверяет были от вет пользователя верным. """
        if len(right_answers) == len(user_answers):
            for ind, value in enumerate(right_answers):
                if user_answers[ind] != value:
                    return False
            return True
        return False

    def save_result_to_db(self, user, quiz, result):
        """ Сохраняет результаты теста в БД """
        user_quiz_results, _ = UserQuizResults.objects.get_or_create(
            user_profile=user,
            quiz=quiz
        )
        if result:
            right_answers = user_quiz_results.right_answers_quantity
            right_answers += 1
            user_quiz_results.right_answers_quantity = right_answers
        else:
            wrong_answers = user_quiz_results.wrong_answers_quantity
            wrong_answers += 1
            user_quiz_results.wrong_answers_quantity = wrong_answers
        user_quiz_results.save()

    def answer_handler(self, right_answers, user_answers, user, quiz):
        result = self.is_right_answer(right_answers, user_answers)
        self.save_result_to_db(user=user, quiz=quiz, result=result)

    def get_page_quiz_id_question_id(self, data_from_templates):
        """
        Возвращает номер страницы, с которой пришел post-запрос, PK текущего теста и текущего вопроса.
        Оба параметра передаются из шаблона passing.html.
        """
        data = [el.split(',') for el in data_from_templates]
        page, quiz_pk, question_pk, *_ = data[0]
        page = 1 if page is None else page
        return page, quiz_pk, question_pk

    def get_questions_id(self, questions) -> tuple:
        """ Возвращает PK всех вопросов из QuerySet """
        questions_id = [question.id for question in questions]
        return tuple(questions_id)

    def get_answers_from_db(self, questions_id: tuple) -> tuple:
        """ Возвращает кортеж из ответов ко всем вопросам теста tuple(tuple(), tuple(), tuple() ...)"""
        answers = list()
        for question_id in questions_id:
            answers_queryset = Answer.objects.filter(question=question_id)  # все ответы на конкретный вопрос теста
            answers.append(tuple([answer for answer in answers_queryset]))
        return tuple(answers)

    def add_pagination(self, request, questions_queryset, page_number=None) -> dict:
        """ Пагинатор для постраничного вывода вопросов """
        paginator = Paginator(questions_queryset, 1)
        if request.method == 'GET':
            page = request.GET.get('page')
        else:
            page = page_number
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)
        return {'page': page, 'questions': questions}


class QuizResultsView(View):
    def get(self, request):
        quiz_pk = request.GET.get('quiz_pk')
        user = request.user
        right_answers, wrong_answers, percent = self.get_results(user=user, quiz_pk=quiz_pk)
        context = {
            'right_answers': right_answers,
            'wrong_answers': wrong_answers,
            'percent': percent,
        }
        return render(request, 'quiz/results.html', {'context': context, 'menu': MENU})

    def get_results(self, user, quiz_pk):
        """
        Возвращает количество верных/неверных ответов + процент верных ответов по итогам прохождения конкретного теста.
        Обнуляет результаты теста в БД.
        """
        quiz_results = UserQuizResults.objects.get(user_profile=user, quiz=Quiz.objects.get(id=quiz_pk))
        right = quiz_results.right_answers_quantity
        wrong = quiz_results.wrong_answers_quantity
        total_questions = right + wrong
        result_in_percent = int(right * 100 / total_questions)
        quiz_results.right_answers_quantity, quiz_results.wrong_answers_quantity = 0, 0
        quiz_results.save()
        return right, wrong, result_in_percent


class AboutView(View):
    def get(self, request):
        return render(request, 'quiz/about.html', {'menu': MENU})


class OfferView(View):
    def get(self, request):
        return render(request, 'quiz/offer.html', {'menu': MENU})


class UserLoginView(LoginView):
    template_name = 'quiz/login.html'
    next_page = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu'] = MENU
        return context


class UserLogoutView(LogoutView):
    template_name = 'quiz/logout.html'
    next_page = reverse_lazy('index')


class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm
        return render(request, 'quiz/registr.html', {'form': form, 'menu': MENU})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        return render(request, 'quiz/registr.html', {'form': form})


def custom_page_not_found_view(request, exception):
    return HttpResponseNotFound('Мы не можем найти такую страницу')
