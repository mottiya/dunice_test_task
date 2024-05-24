from enum import Enum

from django.conf import settings
from django.db import models


class Poll(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.pk}: {self.title}'


class QuestionTypeEnum(Enum):
    ONE_CHOOSE = 1
    MANY_COOSE = 2


class QuestionType(models.Model):
    description = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'{self.pk}: {self.description}'


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question_type = models.ForeignKey(QuestionType, on_delete=models.PROTECT)
    question_text = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.pk}: {self.question_text[:30]}...'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, through="AnswerUser")

    def __str__(self) -> str:
        return f'{self.pk}: {self.answer_text[:30]}...'


class AnswerUser(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'user: {self.user_id}, answer: {self.answer_id}'
