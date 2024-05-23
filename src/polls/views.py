from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError

from .utils import PollService
from .serializers import (
    # PollSerializer,
    # QuestionTypeSerializer,
    # QuestionSerializer,
    # AnswerSerializer,
    AnswerUserSerializer,
)


@api_view(http_method_names=['GET'])
def get_polls_by_user_id_view(request: Request, user_id: str) -> Response:
    response_data = PollService().get_polls_by_user_id(user_id=user_id)
    return Response({'polls': response_data})


@api_view(http_method_names=['POST'])
def add_answer_user_view(request: Request) -> Response:
    serializer = AnswerUserSerializer(data=request.data)
    if not serializer.is_valid() or PollService().is_can_add_answer_user(
            serializer.validated_data['user'].id,
            serializer.validated_data['answer'].id):
        raise ValidationError(detail="You cannot add an answer to this question")
    serializer.save()
    return Response(serializer.data)
