from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from dashboard.models import Quiz

class Result(models.Model):
    percentage = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        get_user_model(), related_name='results', on_delete=models.CASCADE)
    time_spent = models.DurationField(default=0)
    no_of_questions_answered = models.IntegerField(default=0)
    no_of_correct_choices_answered = models.IntegerField(default=0)
    no_of_questions= models.IntegerField(default=0)
    quiz = models.ForeignKey(Quiz, 
        related_name='results', 
        on_delete=models.CASCADE,
    )
    date = models.DateField(default = timezone.now)
    
    def __str__(self):
        return f'{self.percentage}'
