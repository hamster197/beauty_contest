from django.urls import path

from apps.tours_vote.views import *

app_name = 'tours_votes'

urlpatterns = [
    path('', MainVote.as_view(), name='index'),
    path('results/', VoteResult.as_view(), name='results'),
]