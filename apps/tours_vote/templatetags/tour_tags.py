from django import template


register = template.Library()

@register.simple_tag()
def get_tour_estimation(instance, item):
    try:
        estimation = instance.tour_vote_results_participant_id.all().get(tours_question_type_id=item).estimation
    except:
        estimation = 0
    return estimation

@register.simple_tag()
def get_tour_sum_estimation(instance, ):
    from django.db.models import Sum
    return instance.tour_vote_results_participant_id.all().aggregate(Sum('estimation'))