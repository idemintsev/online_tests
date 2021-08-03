from django.urls import path

from django.conf.urls.static import static
from online_tests import settings
from quiz.views import Index, QuizView, UserLoginView, UserLogoutView, AboutView, OfferView, UserRegisterView


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('quiz/<int:pk>/', QuizView.as_view(), name='quiz'),
    path('about/', AboutView.as_view(), name='about'),
    path('offer/', OfferView.as_view(), name='offer'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
