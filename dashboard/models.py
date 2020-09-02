from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Story(models.Model):
    story_title = models.CharField(max_length=100)
    story_text = models.TextField()

    def get_absolute_url(self):
        return reverse('dash:story-detail', args=[self.pk, ])

    def __str__(self):
        return self.story_title


class Question(models.Model):
    question_text = models.CharField(max_length=250)
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name='questions')

    def get_absolute_url(self):
        return reverse('dash:question-detail', args=[self.pk, ])

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
    users = models.ManyToManyField(
        get_user_model(), related_name='choices')
    mark = models.CharField(
        max_length=5, choices=MARK, default='wrong')

    # def get_absolute_url(self):
    #     return reverse('dash:question-list')

    def __str__(self):
        return self.choice_text
