from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponseNotFound
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from quiz.models import Quiz
from quiz.forms import UserRegisterForm


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


class QuizView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz.html'
    context_object_name = 'content'


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
