from django.core.validators import MaxValueValidator
from django.db import models

from users.models import MainUser


# Create your models here.
def get_user_from_request():
    import inspect
    request = [
        frame_record[0].f_locals["request"]
        for frame_record in inspect.stack()
        if frame_record[3] == "get_response"
    ][0]
    return request.user

# Create your models here.
class TourType(models.Model):
    title = models.CharField('Название', max_length=45, unique=True, )
    order = models.PositiveIntegerField('Порядок', unique=True)

    class Meta:
        verbose_name = 'Справочник Конкурс'
        verbose_name_plural = 'Справочник Конкурс'
        ordering = ['order']

    def __str__(self):
        return self.title

class ToursQuestionType(models.Model):
    tour = models.ForeignKey(TourType, verbose_name='Конкурс', on_delete=models.CASCADE, related_name='tours_question_type_id')
    title = models.CharField('Название', max_length=45, unique=True, )
    max_estimation = models.PositiveIntegerField('Максимальная оценка',)

    class Meta:
        verbose_name = 'Справочник типов ответов'
        verbose_name_plural = 'Справочник типов ответов'

    def __str__(self):
        return self.title

def get_tours():
    return [c.id for c in TourType.objects.all()]

class VoteGuide(models.Model):
    title = models.CharField('Название', max_length=50, unique=True, )
    creation_date = models.DateTimeField('Дата создания', auto_now_add=True)
    tours = models.ManyToManyField(TourType, verbose_name='Конкурсы', related_name='vote_quide_tour_id', default=get_tours())

    class Meta:
        verbose_name = 'Справочник голосования'
        verbose_name_plural = 'Справочник голосования'
        ordering = ['-pk']

    def __str__(self):
        return self.title

    def get_active_vote():
        if not VoteGuide.objects.exists():
            VoteGuide.objects.create(title='First vote')

        return VoteGuide.objects.all().first()

class VoteParticipants(models.Model):
    vote_id = models.ForeignKey(VoteGuide, verbose_name='Голосование', related_name='participants_vote_id',
                                on_delete=models.CASCADE, default=VoteGuide.get_active_vote().pk)
    full_name = models.CharField('ФИО', max_length=255)
    photo = models.ImageField('Фото', upload_to='photo/', )
    user_id = models.PositiveIntegerField('Hомер участника', )

    def __str__(self):
        return str(self.vote_id) + ' ' + self.full_name

    class Meta:
        verbose_name = 'Участники голосования'
        verbose_name_plural = 'Участник голосования'
        constraints = [
            models.UniqueConstraint(fields=['vote_id_id', 'user_id'], name='unique_participants_vote_id_id__user_id')
        ]

class VoteResults(models.Model):
    user_id  = models.ForeignKey(MainUser, verbose_name='Проголосовал', related_name='tour_vote_results_user_id',
                                 on_delete=models.CASCADE, limit_choices_to={"is_active": True, 'groups__name': 'Jury'},)
    vote_id = models.ForeignKey(VoteGuide, verbose_name='Голосование', related_name='tour_vote_results_vote_id',
                                on_delete=models.CASCADE, default=VoteGuide.get_active_vote().pk)
    tours_question_type_id = models.ForeignKey(ToursQuestionType, verbose_name='Тип конкурса', on_delete=models.CASCADE,
                                               related_name='tour_vote_results_question_type_id')
    participant_id = models.ForeignKey(VoteParticipants, verbose_name='За кого', related_name='tour_vote_results_participant_id',
                                 on_delete=models.CASCADE, limit_choices_to={'vote_id':VoteGuide.get_active_vote().pk})
    estimation = models.PositiveIntegerField('Оценка', validators=[MaxValueValidator(3)])

    class Meta:
        verbose_name = 'Результаты голосования'
        verbose_name_plural = 'Результаты голосования'
        constraints = [
            models.UniqueConstraint(fields=['tours_question_type_id', 'user_id', 'participant_id'],
                                    name='unique_tour__results_vote_id_id__user_id')
        ]

class VoteStep(models.Model):
    user_id = models.ForeignKey(MainUser, verbose_name='Проголосовал', related_name='vote_step_user_id',
                                on_delete=models.CASCADE,
                                limit_choices_to={"is_active": True, 'groups__name': 'Jury'}, )
    vote_id = models.ForeignKey(VoteGuide, verbose_name='Голосование', related_name='vote_step_vote_id',
                                on_delete=models.CASCADE, default=VoteGuide.get_active_vote().pk)
    step = models.PositiveIntegerField('Шаг', default=0)
