from django.urls import path

from apps.votes.views import MainVote

app_name = 'votes'

urlpatterns = [
    path('', MainVote.as_view(), name='index')
]