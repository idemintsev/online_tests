from django.urls import path
from check_knowledge.views import (
    MainPage, RegistrationUser, AuthView, Logout,
)


urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('registration/', RegistrationUser.as_view(), name='registration'),
    path('login/', AuthView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
