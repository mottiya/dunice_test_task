from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

poll_list = views.RetrieveListCreatePollsView.as_view({
    'get': 'list',
    'post': 'create',
})
poll_retrieve = views.RetrieveListCreatePollsView.as_view({
    'get': 'retrieve',
})
answer_list = views.ListCreateAnswerUsersView.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = format_suffix_patterns([
    path('polls/', poll_list, name='poll-list'),
    path('polls/user/<int:user_id>/', poll_retrieve, name='poll-retrieve'),
    path('answer/', answer_list, name='answer-list'),
])
