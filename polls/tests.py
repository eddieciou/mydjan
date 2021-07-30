import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question, Choice


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_old_question(self):
        old_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=old_time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        recent_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=recent_time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_feature_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """

        future_time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=future_time)
        self.assertIs(future_question.was_published_recently(), False)


def create_question(question_text, days, have_choice=True):
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(
        question_text=question_text,
        pub_date=time
    )

    if have_choice:
        Choice.objects.create(
            question=question,
            choice_text='Default_choice_1'
        )
        Choice.objects.create(
            question=question,
            choice_text='Default_choice_2'
        )

    return question


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        question = create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_future_question(self):
        create_question("Future question", days=10)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        question = create_question("Past question", days=-30)
        create_question("Future question", days=10)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_two_past_question(self):
        question1 = create_question("Past question1", days=-10)
        question2 = create_question("Past question1", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [question2, question1])

    def test_have_not_choice_question(self):
        create_question("Have not choice question", days=-1, have_choice=False)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


class QuestionDetailViewTests(TestCase):
    def test_past_question(self):
        question = create_question("Past question", days=-10)
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)

    def test_future_question(self):
        question = create_question("Future question", days=10)
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 404)


class QuestionResultViewTests(TestCase):
    def test_past_question(self):
        question = create_question("Past question", days=-10)
        response = self.client.get(reverse('polls:results', args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)

    def test_future_question(self):
        question = create_question("Future question", days=10)
        response = self.client.get(reverse('polls:results', args=(question.id,)))
        self.assertEqual(response.status_code, 404)
