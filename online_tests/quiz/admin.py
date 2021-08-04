from django.contrib import admin
from quiz.models import Quiz, Question, Answer


class QuestionInLine(admin.TabularInline):
    model = Question


class AnswerInLine(admin.TabularInline):
    model = Answer

class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject', 'update_at']
    list_filter = ['created_date', 'update_at', 'name', 'subject']
    search_fields = ['name', 'subject']
    inlines = [QuestionInLine]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', ]
    list_filter = ['quiz', ]
    search_fields = ['quiz', 'text', ]
    inlines = [AnswerInLine]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'status']
    list_filter = ['status']
    search_fields = ['text']


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
