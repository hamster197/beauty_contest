from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.tours_vote.models import *

# Register your models here.
@admin.register(VoteGuide)
class VoteParticipantsAdmin(ModelAdmin):
    list_display = ('pk', 'title',)

@admin.register(TourType)
class VoteParticipantsAdmin(ModelAdmin):
    list_display = ('pk', 'title', 'order', )

@admin.register(ToursQuestionType)
class VoteParticipantsAdmin(ModelAdmin):
    list_display = ('pk', 'tour', 'title', 'max_estimation', )
    list_filter = ('tour',)

@admin.register(VoteParticipants)
class VoteParticipantsAdmin(ModelAdmin):
    list_display = ('pk', 'vote_id', 'full_name', 'user_id', )
    list_filter = ('vote_id',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if obj:
            form.base_fields['vote_id'].disabled = True
        return form

@admin.register(VoteResults)
class VoteResultsAdmin(ModelAdmin):
    list_display = ('pk', 'vote_id', 'tours_question_type_id', 'participant_id', 'user_id', 'estimation',)
    list_filter = ('vote_id',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if obj:
            form.base_fields['vote_id'].disabled = True
        return form

@admin.register(VoteStep)
class VoteStepAdmin(ModelAdmin):
    list_display = ('pk', 'user_id', 'vote_id', 'step', )
    list_filter = ('user_id', 'vote_id')