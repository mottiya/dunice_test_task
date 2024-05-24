from django.urls import path

from . import views

urlpatterns = [
    path('polls/<int:user_id>/', views.get_polls_by_user_id_view),
    path('answer/', views.add_answer_user_view),
    path('get_answer/', views.get_answer_user_by_poll_view),
    path('polls/', views.get_most_complited_polls_view),
    path('polls/create', views.create_poll_view)
]
