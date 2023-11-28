from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.votes.models import VoteParticipants, VoteGuide, VoteResults

admin.site.register(VoteGuide)

@admin.register(VoteParticipants)
class VoteParticipantsAdmin(ModelAdmin):
    list_display = ('pk', 'vote_id', 'full_name', 'user_id', )
    list_filter = ('vote_id',)
    #readonly_fields = ['vote_id']

@admin.register(VoteResults)
class VoteResultsAdmin(ModelAdmin):
    list_display = ('pk', 'vote_id', 'participant_id', 'user_id', 'estimation',)
    list_filter = ('vote_id',)
    #readonly_fields = ['vote_id']

# admin.site.register(VoteResults)