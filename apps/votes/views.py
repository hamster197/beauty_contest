from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from apps.votes.models import VoteParticipants, VoteGuide, VoteResults


# Create your views here.
class MainVote(LoginRequiredMixin, ListView):
    template_name = 'votes/index.html'
    context_object_name = 'instances'

    def get_queryset(self):
        return VoteParticipants.objects.filter(vote_id=VoteGuide.objects.all().last())#.order_by('estimation__sum')

    def post(self, request, *args, **kwargs):
        if self.request.user.groups.get().name == 'Jury':
            for item in self.get_queryset():
                VoteResults.objects.update_or_create(participant_id=item, vote_id=item.vote_id,
                                                     user_id=self.request.user,
                                                     defaults={"estimation": self.request.POST.get(str(item.pk))})
        return self.get(request)


