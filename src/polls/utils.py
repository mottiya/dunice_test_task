from typing import Dict, Any, List

from django.db import DatabaseError, transaction
from django.db.models import Q, Subquery, Count

from .models import (
    Poll,
    Question,
    Answer,
    AnswerUser,
    QuestionTypeEnum
)


class PollService():

    def get_polls_by_user_id(self, user_id: int) -> Poll:
        """
        Получить все опросы которые проходил пользователь\n
        sql:\n
        SELECT *
            FROM "polls_poll"
            WHERE "polls_poll"."id" IN (
                SELECT DISTINCT U2."poll_id"
                FROM "polls_answer" U0
                INNER JOIN "polls_answeruser" U1 ON (U0."id" = U1."answer_id")
                INNER JOIN "polls_question" U2 ON (U0."question_id" = U2."id")
                WHERE U1."user_id" = 2
            )
        """
        subquery_poll_id = Answer.objects.filter(users=user_id).select_related('question__poll').values('question__poll_id').distinct()
        return Poll.objects.filter(id__in=Subquery(subquery_poll_id))

    def is_can_add_answer_user(self, user_id: int, answer_id: int) -> bool:
        """
        Проверяет можно ли вставить ответ на вопрос для пользователя\n
        sql:\n
        SELECT *
        FROM "polls_answer"
        INNER JOIN "polls_answeruser" ON ("polls_answer"."id" = "polls_answeruser"."answer_id")
        INNER JOIN "polls_question" ON ("polls_answer"."question_id" = "polls_question"."id")
        WHERE
            "polls_answeruser"."user_id" = 1
            AND (
                "polls_answer"."id" = 7
                OR (
                    "polls_question"."question_type_id" = 1
                    AND "polls_answer"."question_id" = (
                        SELECT U0."question_id"
                        FROM "polls_answer" U0
                        WHERE U0."id" = 7
                        LIMIT 1
                    )
                )
            )
        """
        result = Answer.objects.select_related('question').filter(users=user_id).filter(
            Q(question__question_type_id=QuestionTypeEnum.ONE_CHOOSE.value,
              question_id=Subquery(Answer.objects.filter(id=answer_id).values('question_id')[:1])) | Q(id=answer_id)
        )
        return not result.exists()

    def get_answer_user_by_poll(self, user_id: int, poll_id: int) -> AnswerUser:
        """
        Получить все ответы пользователя по опросу
        sql:\n
        SELECT *
            FROM "polls_answeruser"
            INNER JOIN "polls_answer" ON ("polls_answeruser"."answer_id" = "polls_answer"."id")
            INNER JOIN "polls_question" ON ("polls_answer"."question_id" = "polls_question"."id")
            WHERE ("polls_answeruser"."user_id" = 1 AND "polls_question"."poll_id" = 1)
        """
        return AnswerUser.objects.select_related('answer__question').filter(user_id=user_id).filter(answer__question__poll_id=poll_id)

    def get_most_complited_polls(self, count: int = 5) -> Poll:
        """
        Получить наиболее часто проходимые опросы.
        sql:\n
        SELECT "polls_poll"."id",
               "polls_poll"."user_id",
               "polls_poll"."title",
               "polls_poll"."created_at",
               COUNT(DISTINCT "polls_answeruser"."id") AS "num_users"
            FROM "polls_poll"
            LEFT OUTER JOIN "polls_question" ON ("polls_poll"."id" = "polls_question"."poll_id")
            LEFT OUTER JOIN "polls_answer" ON ("polls_question"."id" = "polls_answer"."question_id")
            LEFT OUTER JOIN "polls_answeruser" ON ("polls_answer"."id" = "polls_answeruser"."answer_id")
            GROUP BY "polls_poll"."id"
            ORDER BY 5 DESC
            LIMIT 5
        """
        return Poll.objects.annotate(
            num_users=Count('question__answer__answeruser', distinct=True)
        ).order_by('-num_users')[:count]

    def create_poll_with_related_entities(self, data: Dict[str, str | List]) -> Poll | None:
        """
        Создает опрос и все связанные в нем сущьности из переданных данных в одной транзакции
        """
        try:
            with transaction.atomic():
                questions_data: List[Dict[str, Any]] = data.pop('questions')
                poll = Poll.objects.create(**data)
                for question_data in questions_data:
                    answers_data = question_data.pop('answers')
                    question = Question.objects.create(poll=poll, **question_data)
                    for answer_data in answers_data:
                        Answer.objects.create(question=question, **answer_data)
                return poll
        except DatabaseError:
            return None
