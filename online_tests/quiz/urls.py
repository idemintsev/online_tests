from django.urls import path

from django.conf.urls.static import static
from online_tests import settings
from quiz.views import Index, categories


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('categories/<int:quiz_id>/', categories, name='categories'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)