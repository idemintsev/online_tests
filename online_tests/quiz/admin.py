from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from quiz.forms import AnswerInLineFormset
from quiz.models import Quiz, Question, Answer, UserQuizResults


class QuestionInLine(admin.TabularInline):
    model = Question
    show_change_link = True  # добавляет ссылку на форму изменения


class AnswerInLine(admin.TabularInline):
    model = Answer
    formset = AnswerInLineFormset


class UserQuizResultsInLine(admin.StackedInline):
    model = UserQuizResults
    can_delete = False
    verbose_name = 'Информация о прохождении тестов'
    exclude = ['quiz', ]


class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject', 'update_at', 'view_questions_link', ]
    list_filter = ['created_date', 'update_at', 'name', 'subject']
    list_display_links = ['name', ]
    search_fields = ['name', 'subject']
    # inlines = [QuestionInLine]
    fields = ['name', 'subject']

    def get_question(self, obj):
        return obj.question.text

    def get_answer(self, obj):
        return obj.question.answer

    def view_questions_link(self, obj):
        """
        Создает в админке в разделе Тесты колноку-ссылку на перечень вопросов к конкретному тесту.
        """
        count = obj.question.count()
        url = (
                reverse('admin:quiz_question_changelist')
                + '?'
                + urlencode({'quiz__id__exact': f'{obj.id}'})
        )
        return format_html('<a href="{}">{} Вопросы</a>', url, count)

    view_questions_link.short_description = "Создать/редактировать вопросы"


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', ]
    list_filter = ['quiz', ]
    inlines = [AnswerInLine]
    list_display_links = ['text', ]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'status']
    list_filter = ['status']
    search_fields = ['text']


class UserQuizResultsAdmin(UserAdmin):
    inlines = (UserQuizResultsInLine,)
    list_display = ['id', 'username', 'first_name', 'last_name', ]
    search_fields = ['username', 'first_name', 'last_name']
    list_display_links = ['username', ]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.unregister(User)
admin.site.register(User, UserQuizResultsAdmin)
