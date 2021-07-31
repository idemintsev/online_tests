from django.contrib import admin

from check_knowledge.models import Test, TestQuestions, TestAnswers


class TestInLine(admin.TabularInline):
    model = Test


class TestQuestionsInLine(admin.TabularInline):
    model = TestQuestions


class TestAnswersInLine(admin.TabularInline):
    model = TestAnswers


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'subject',]
    list_filter = ['created_date', 'update_at', 'name', 'subject']
    search_fields = ['name', 'subject']
    inlines = [TestQuestionsInLine]
    fieldsets = (
        ('Тематика и название теста', {'fields': ('name', 'subject')}),
    )


@admin.register(TestQuestions)
class TestQuestionsAdmin(admin.ModelAdmin):

    list_display = ['id', 'test', 'question']
    list_filter = ['test', 'question']
    search_fields = ['test', 'question']
    inlines = [TestAnswersInLine]
    # fieldsets = (
    #     ('Тематика и название теста', {'fields': ('test', 'question')}),
    # )
