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

from collections import defaultdict


menu = [{'title': 'О проекте', 'url_name': 'about'},
        {'title': 'Предложить тест', 'url_name': 'offer'},]


class Index(ListView):
    model = Quiz
    template_name = 'quiz/index.html'
    context_object_name = 'quizzes_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
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
        """
        quiz_pk = request.GET.get('quiz_pk')
        questions_queryset = Question.objects.filter(quiz_id=quiz_pk)
        context = self.add_pagination(request, questions_queryset)
        context.update({'quiz_pk': quiz_pk})
        return render(request, 'quiz/passing.html', context)

    def add_pagination(self, request, questions_queryset) -> dict:
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
