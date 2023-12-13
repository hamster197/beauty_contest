from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Sum
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from apps.tours_vote.models import *
from users.decorators import leader_check


# Create your views here.
leader_decorators = [login_required, user_passes_test(leader_check)]

class MainVote(LoginRequiredMixin, ListView):
    template_name = 'tours_votes/vote.html'
    context_object_name = 'instances'
    active_vote = VoteGuide.get_active_vote()

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name='Jury').exists():
            return redirect('tours_votes:results')
        return super(MainVote, self).dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        if hasattr(self, "get") and not hasattr(self, "head"):
            self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.step_instance, created = VoteStep.objects.get_or_create(user_id=self.request.user, vote_id=self.active_vote)
        self.active_tour = self.active_vote.tours.all()[self.step_instance.step]

    def get_queryset(self):
        queryset = VoteParticipants.objects.filter(vote_id=self.active_vote.pk)\
            .prefetch_related(Prefetch('tour_vote_results_participant_id',
                                       VoteResults.objects.filter(vote_id=self.active_vote, user_id=self.request.user)))

        return queryset

    def post(self, request, *args, **kwargs):
        if '_next_step' in self.request.POST:
            if self.step_instance.step < self.active_vote.tours.all().count() - 1:
                self.step_instance.step += 1
                self.step_instance.save()

        if '_previous_step' in self.request.POST:
            if self.step_instance.step > 0:
                self.step_instance.step -= 1
                self.step_instance.save()

        if '_get_estimation' in self.request.POST:
            for user in self.get_queryset():
                for tour in self.active_tour.tours_question_type_id.all():
                    estimation = self.request.POST.get(str(user.pk) + '_' + str(tour.pk))
                    if estimation is not None and estimation.isdigit():
                        if int(estimation) <= tour.max_estimation:
                            VoteResults.objects.update_or_create(participant_id=user, vote_id=self.active_vote,
                                                                 user_id=self.request.user,
                                                                 tours_question_type_id=tour,
                                                                 defaults={"estimation": estimation})


        return redirect('tours_votes:index')

@method_decorator(leader_decorators, name='dispatch')
class VoteResult(LoginRequiredMixin, ListView):
    template_name = 'tours_votes/result.html'
    context_object_name = 'instances'
    active_vote = VoteGuide.get_active_vote()

    def get_queryset(self):
        queryset = VoteParticipants.objects.filter(vote_id=self.active_vote.pk) \
            .prefetch_related(Prefetch('tour_vote_results_participant_id',
                                       VoteResults.objects.filter(vote_id=self.active_vote,)))

        return queryset.values('full_name', 'user_id').annotate(Sum('tour_vote_results_participant_id__estimation'))\
            .order_by('-tour_vote_results_participant_id__estimation__sum')
