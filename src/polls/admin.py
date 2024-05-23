from django.contrib import admin
from .models import Poll, QuestionType, Question, Answer, AnswerUser


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'poll_id', 'question_type', 'question_text', 'created_at')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_id', 'answer_text', 'created_at')


@admin.register(AnswerUser)
class AnswerUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'answer_id')
