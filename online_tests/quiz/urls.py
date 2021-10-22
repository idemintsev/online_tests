import debug_toolbar
from django.conf.urls.static import static
from django.urls import path, include

from online_tests import settings
from quiz.views import (
    IndexView, QuizView, UserLoginView, UserLogoutView, AboutView, OfferView, UserRegisterView, QuizPassingView,
    QuizResultsView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('quiz/<int:pk>/', QuizView.as_view(), name='quiz'),
    path('passing', QuizPassingView.as_view(), name='passing'),
    path('about/', AboutView.as_view(), name='about'),
    path('offer/', OfferView.as_view(), name='offer'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('results/', QuizResultsView.as_view(), name='results'),
    path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
