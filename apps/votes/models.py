from django.core.validators import MaxValueValidator
from django.db import models

from users.models import MainUser

def get_user_from_request():
    import inspect
    request = [
        frame_record[0].f_locals["request"]
        for frame_record in inspect.stack()
        if frame_record[3] == "get_response"
    ][0]
    return request.user

# Create your models here.
class VoteGuide(models.Model):
    title = models.CharField('Название', max_length=50)
    creation_date = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Справочник голосования'
        verbose_name_plural = 'Справочник голосования'

if not VoteGuide.objects.exists():
    VoteGuide.objects.create(title='First vote')

active_vote = VoteGuide.objects.all().last().pk

class VoteParticipants(models.Model):
    vote_id = models.ForeignKey(VoteGuide, verbose_name='Голосование', related_name='participants_vote_id',
                                on_delete=models.CASCADE, default=active_vote)
    full_name = models.CharField('ФИО', max_length=255)
    photo = models.ImageField('Фото', upload_to='photo/', )
    user_id = models.PositiveIntegerField('Hомер участника', )

    def __str__(self):
        return str(self.vote_id) + ' ' + self.full_name

    def get_user_estimation(self):
        return VoteResults.objects.filter(participant_id_id=self.pk, user_id=get_user_from_request(), vote_id=self.vote_id, )

    def get_participant_estimation(self):
        from django.db.models import Sum
        return VoteResults.objects.filter(participant_id_id=self.pk, vote_id=self.vote_id, ).aggregate(Sum('estimation'))

    class Meta:
        verbose_name = 'Участники голосования'
        verbose_name_plural = 'Участник голосования'
        constraints = [
            models.UniqueConstraint(fields=['vote_id_id', 'user_id'], name='unique_participants_vote_id_id__user_id')
        ]

class VoteResults(models.Model):
    user_id  = models.ForeignKey(MainUser, verbose_name='Проголосовал', related_name='votevesults_user_id',
                                 on_delete=models.CASCADE, limit_choices_to={"is_active": True, 'groups__name': 'Jury'},)
    vote_id = models.ForeignKey(VoteGuide, verbose_name='Голосование', related_name='votevesults_vote_id',
                                on_delete=models.CASCADE, default=active_vote)
    participant_id = models.ForeignKey(VoteParticipants, verbose_name='За кого', related_name='votevesults_participant_id',
                                 on_delete=models.CASCADE, limit_choices_to={'vote_id':active_vote})
    estimation = models.PositiveIntegerField('Оценка', validators=[MaxValueValidator(3)])

    class Meta:
        verbose_name = 'Результаты голосования'
        verbose_name_plural = 'Результаты голосования'
        constraints = [
            models.UniqueConstraint(fields=['vote_id_id', 'user_id', 'participant_id'],
                                    name='unique_resultatss_vote_id_id__user_id')
        ]

    def __str__(self):
        return str(self.estimation)