from datetime import timedelta

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Quiz(models.Model):
    quiz_title = models.CharField(max_length=100)
    quiz_text = models.TextField()
    duration = models.DurationField(default=timedelta(minutes=5), help_text='HH:MM:SS')

    def get_absolute_url(self):
        return reverse('dash:quiz_detail', args=[self.pk, ])

    def get_delete_url(self):
        return reverse('dash:quiz_delete', args=[self.pk, ])

    def get_update_url(self):
        return reverse('dash:quiz_update', args=[self.pk, ])

    def __str__(self):
        return self.quiz_title


class Question(models.Model):
    question_text = models.TextField()
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='questions')

    def get_absolute_url(self):
        return reverse('dash:question_detail', args=[self.pk, ])

    def get_delete_url(self):
        return reverse('dash:question_delete', args=[self.pk, ])

    def get_update_url(self):
        return reverse('dash:question_update', args=[self.pk, ])

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    MARK = (
        ('right', 'Right'),
        ('wrong', 'Wrong'),
    )
    choice_text = models.CharField(max_length=250)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='choices')    
    mark = models.CharField(
        max_length=5, 
        choices=MARK, 
        default='wrong',
        help_text='is this the right or wrong choice for this question? ',
    )    

    def get_update_url(self):
        return reverse('dash:choice_update', args=[self.pk, ])

    def __str__(self):
        return self.choice_text
