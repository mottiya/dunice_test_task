from rest_framework import serializers
from .models import Poll, Question, QuestionType, Answer, AnswerUser


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class AnswerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerUser
        fields = '__all__'
