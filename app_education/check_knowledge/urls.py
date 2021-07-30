from django.urls import path
from check_knowledge.views import MainPage


urlpatterns = [
    path('', MainPage.as_view(), name='main'),
]
