from django.urls import path

from . import views

urlpatterns = [
    path('polls/<int:user_id>', views.get_polls_by_user_id_view),
    path('answer', views.add_answer_user_view)
]
