# Base python imports
import datetime

# Django imports
from django.db import models
from django.utils import timezone

# Question model
#
# Attribs:
# question_text: String of length 200
# pub_date: Timestamp
class Question(models.Model): # extends Model
    # Defines actions to take when an instance of this model
    # needs to be printed / output in some fashion.
    def __str__(self):
        return self.question_text

    # Was this question published recently?
    def was_published_recently(self):
        now = timezone.now()

        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

# Choice model
#
# Attribs:
# question: Question (FK)
# choice_text: String of length 200
# votes: Integer (default of 0)
class Choice(models.Model):
    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
