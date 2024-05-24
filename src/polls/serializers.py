from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Poll, Question, QuestionType, Answer, AnswerUser
from .utils import PollService


class AnswerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerUser
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    answerusers = AnswerUserSerializer(many=True, required=False)
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)

    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=False)
    poll = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.all(), required=False)

    class Meta:
        model = Question
        fields = '__all__'


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Poll
        fields = '__all__'

    def create(self, validated_data):
        return PollService().create_poll_with_related_entities(validated_data)
