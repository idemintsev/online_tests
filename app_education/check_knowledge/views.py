from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib.auth import authenticate, login
from check_knowledge.models import Test, Profile
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from check_knowledge.forms import RegisterForm


class MainPage(generic.ListView):

    model = Test
    template_name = 'site/main_page.html'
    context_object_name = 'tests_list'


class TestDetailView(generic.DetailView):

    model = Test
    template_name = 'site/test_details.html'
    context_object_name = 'details'


class RegistrationUser(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/registration.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            Profile.objects.create(
                user=user,
                email=email
            )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main')
        else:
            return render(request, 'users/registration.html', {'form': form})


class AuthView(LoginView):
    template_name = 'users/login.html'
    next_page = reverse_lazy('main')


class Logout(LogoutView):
    template_name = 'users/logout.html'
    next_page = reverse_lazy('main')
