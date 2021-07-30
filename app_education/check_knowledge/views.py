from django.shortcuts import render
from django.views import generic

from check_knowledge.models import Test


class MainPage(generic.ListView):

    model = Test
    template_name = 'site/main_page.html'
    context_object_name = 'tests_list'
