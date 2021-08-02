from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.http import HttpResponse, HttpResponseNotFound

class Index(View):

    def get(self, request):
        return render(request, 'index.html', {'context': 'Главная страница'})


def categories(request, quiz_id):
    return HttpResponse(f'Категории {quiz_id}')


def custom_page_not_found_view(request, exception):
    return HttpResponseNotFound('Мы не можем найти такой страницы')
