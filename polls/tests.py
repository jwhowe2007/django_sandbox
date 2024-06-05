import datetime

from django.test import TestCase    # NB: this is an interface to the unittest Python module.
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days_published_offset):
    # Create a question with question_text and number of days in the past or future for its publish date.
    time = timezone.now() + datetime.timedelta(days=days_published_offset)
    return Question.objects.create(question_text=question_text, pub_date=time)

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

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        # No questions - should return an empty set and an informative message.
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")

        self.assertQuerySetEqual(response.context["latest_questions"], [])

    def test_past_question(self):
        # Past questions - all of these should be displayed.
        question = create_question(question_text="Past question test", days_published_offset=-30)
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["latest_questions"], [question])

    def test_future_question(self):
        # Future questions - none of these should be displayed be default.
        create_question(question_text="Future question.", days_published_offset=30)
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_questions"], [])

    def test_future_question_and_past_question(self):
        question = create_question(question_text="Past question.", days_published_offset=-30)
        create_question(question_text="Future question.", days_published_offset=30)

        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_questions"], [question])

    def test_two_past_questions(self):
        question1 = create_question(question_text="Past question 1.", days_published_offset=-30)
        question2 = create_question(question_text="Past question 2.", days_published_offset=-5)

        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_questions"], [question2, question1])
