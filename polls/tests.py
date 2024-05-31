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
