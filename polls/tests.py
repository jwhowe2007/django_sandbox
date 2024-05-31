import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_in_future(self):
        # Check to see if was_published_recently returns False for pub_dates in the future.
        future_date = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=future_date)

        self.assertIs(future_question.was_published_recently(), False)
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)

        # Make sure the behaviour holds for older questions (publish date more than 1 day old)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23,
        minutes=59, seconds=59)

        # Make sure the method holds for recent questions
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
