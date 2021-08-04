from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls'))
]

handler404 = 'quiz.views.custom_page_not_found_view'
