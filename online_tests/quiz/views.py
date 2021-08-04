from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponseNotFound
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from quiz.models import Quiz, Question, Answer
from quiz.forms import UserRegisterForm

MENU = [{'title': 'О проекте', 'url_name': 'about'},
        {'title': 'Предложить тест', 'url_name': 'offer'}, ]


class Index(ListView):
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
        return render(request, 'quiz/quiz.html', {'quiz': quiz})


class QuizPassingView(View):
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
            context = self.add_pagination(request, questions_queryset)  # dict {'page': page, 'questions': questions}
            questions_id = self.get_questions_id(questions_queryset)
            answers_text_tuple = self.get_answers_from_db(questions_id)
            # получаем номер индекса нужного кортежа с ответами в answers_text_tuple.
            # answers_text_tuple[0] - кортеж с ответами на 1-й вопрос, answers_text_tuple[1] - 2-й вопрос и т.д.
            answers_index_for_current_question = 0 if context['page'] is None else (int(context['page']) - 1)
            answers = answers_text_tuple[answers_index_for_current_question]
            context.update(quiz_pk=quiz_pk, answers=answers)
            return render(request, 'quiz/passing.html', context)
        return render(request, 'quiz/passing.html')

    def is_questions_for_quiz(self, questions_queryset):
        """ Проверяет есть ли вопросы для теста """
        if len(questions_queryset):
            return True
        return False

    def get_questions_id(self, questions) -> tuple:
        """ Возвращает PK всех вопросов из QuerySet """
        questions_id = [question.id for question in questions]
        return tuple(questions_id)

    def get_answers_from_db(self, questions_id: tuple) -> tuple:
        """ Возвращает кортеж из ответов ко всем вопросам теста tuple(tuple(), tuple(), tuple() ...)"""
        result_answers_text = list()
        for question_id in questions_id:
            answers_queryset = Answer.objects.filter(question=question_id)  # все ответы на конкретный вопрос теста
            result_answers_text.append(tuple([answer.text for answer in answers_queryset]))  # кортеж из текстов ответов
        return tuple(result_answers_text)

    def add_pagination(self, request, questions_queryset) -> dict:
        """ Пагинатор для постраничного вывода вопросов """
        paginator = Paginator(questions_queryset, 1)
        page = request.GET.get('page')
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)
        return {'page': page, 'questions': questions}


class AboutView(View):
    def get(self, request):
        return render(request, 'quiz/about.html')


class OfferView(View):
    def get(self, request):
        return render(request, 'quiz/offer.html')


class UserLoginView(LoginView):
    template_name = 'quiz/login.html'
    next_page = reverse_lazy('index')


class UserLogoutView(LogoutView):
    template_name = 'quiz/logout.html'
    next_page = reverse_lazy('index')


class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm
        return render(request, 'quiz/registr.html', {'form': form})

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
