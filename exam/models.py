from django.db import models
from django.contrib.auth import get_user_model


# class Result(models.Model):
#     score = models.IntegerField(default=0)
#     user = models.ForeignKey(
#         get_user_model(), related_name='results', on_delete=models.CASCADE)
#     timespent = models.DurationField(default=0)
#     failed = models.IntegerField(default=0)
#     passed = models.IntegerField(default=0)

#     def __str__(self):
#         return self.score
