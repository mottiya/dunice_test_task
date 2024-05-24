from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError

from .utils import PollService
from .serializers import (
    PollSerializer,
    AnswerUserSerializer,
)


class ListCreateAnswerUsersView(ViewSet):
    """
    Представление для ответов пользователя (AnswerUser)
    """
    service = PollService()

    def list(self, request: Request) -> Response:
        """
        Принимает user_id и poll_id в query параметрах запроса
        Returns: список ответов пользователя с user_id по опросу с poll_id
        """
        user_id = request.query_params.get('user_id', 0)
        poll_id = request.query_params.get('poll_id', 0)
        answer_user_list = self.service.get_answer_user_by_poll(user_id, poll_id)
        return Response({'answers': AnswerUserSerializer(answer_user_list, many=True).data})

    def create(self, request: Request) -> Response:
        """
        Принимает user и answer в теле запорса (json)
        Returns: новый созданный ответ пользователя
                 400 Bad Request, если нельзя добавить ответ
        """
        serializer = AnswerUserSerializer(data=request.data)
        if not serializer.is_valid() or not self.service.is_can_add_answer_user(
                serializer.validated_data['user'].id,
                serializer.validated_data['answer'].id):
            raise ValidationError(detail="You cannot add an answer to this question")
        serializer.save()
        return Response({'new_answer': serializer.data})


class RetrieveListCreatePollsView(ViewSet):
    """
    Представление для опросов (Polls)
    """
    service = PollService()

    def retrieve(self, request: Request, user_id: int) -> Response:
        """
        Принимает user_id в строке запроса
        Returns: список опросов которые проходил пользователь с user_id
        """
        polls = self.service.get_polls_by_user_id(user_id=user_id)
        return Response({'polls': PollSerializer(polls, many=True).data})

    def list(self, request: Request) -> Response:
        """
        Принимает count ограничение записей в query параметрах запроса
        Returns: список наиболее часто проходимых опросов по убыванию
        """
        try:
            count = int(request.query_params.get('count', 5))
        except ValueError:
            return Response(status=400)
        polls = self.service.get_most_complited_polls(count)
        return Response({'polls': PollSerializer(polls, many=True).data})

    def create(self, request: Request) -> Response:
        """
        Принимает схему создания опроса в теле запроса (json):
        {
            "user": 1,
            "title": "Пятый опрос",
            "questions": [
                {
                    "question_type": 1,
                    "question_text": "Question example text",
                    "answers": [
                        {
                            "answer_text": "Answer example text"
                        },
                        {
                            "answer_text": "Answer example text"
                        }
                    ]
                },
                {
                    "question_type": 2,
                    "question_text": "Question example text",
                    "answers": [
                        {
                            "answer_text": "Answer example text"
                        },
                        {
                            "answer_text": "Answer example text"
                        }
                    ]
                }
            ]
        }
        Returns: новый созданный опрос
                 400 Bad Request, если нельзя добавить опрос
        """
        serializer = PollSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'new_poll': serializer.data})
