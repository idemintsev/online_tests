from django.contrib import admin
from quiz.models import Quiz, Question


class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject', 'update_at']
    list_filter = ['created_date', 'update_at', 'name', 'subject']
    search_fields = ['name', 'subject']



class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', ]
    list_filter = ['quiz', ]
    search_fields = ['quiz', 'text', ]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
