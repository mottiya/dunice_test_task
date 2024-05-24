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
    if not serializer.is_valid() or not PollService().is_can_add_answer_user(
            serializer.validated_data['user'].id,
            serializer.validated_data['answer'].id):
        raise ValidationError(detail="You cannot add an answer to this question")
    serializer.save()
    return Response({'new_answer': serializer.data})


@api_view(http_method_names=['GET'])
def get_answer_user_by_poll_view(request: Request) -> Response:
    user_id = request.query_params['user_id']
    poll_id = request.query_params['poll_id']
    answer_user_list = PollService().get_answer_user_by_poll(user_id, poll_id)
    return Response({'answers': answer_user_list})


@api_view(http_method_names=['GET'])
def get_most_complited_polls_view(request: Request):
    count = int(request.query_params.get('count', 5))
    poll_list = PollService().get_most_complited_polls(count)
    return Response({'polls': poll_list})
