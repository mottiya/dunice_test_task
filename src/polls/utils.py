from django.db.models import Q
from .models import (
    Poll,
    # QuestionType,
    # Question,
    Answer,
    AnswerUser,
    QuestionTypeEnum
)
from .serializers import (
    PollSerializer,
    # QuestionTypeSerializer,
    # QuestionSerializer,
    # AnswerSerializer,
    # AnswerUserSerializer,
)


class PollService():
    def get_polls_by_user_id(self, user_id: int):
        queryset = Poll.objects.filter(user_id=user_id)
        serializer = PollSerializer(queryset, many=True)
        return serializer.data

    def is_can_add_answer_user(self, user_id: int, answer_id: int):
        question_id = Answer.objects.get(id=answer_id).question
        return AnswerUser.objects.select_related('answer__question').filter(
            Q(user_id=user_id) & (
                Q(answer__question__question_type_id=QuestionTypeEnum.ONE_CHOOSE.value,
                  answer__question_id=question_id) | Q(id=answer_id)
            )
        ).exists()
