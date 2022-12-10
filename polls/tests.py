#python
import datetime
#django
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
#models
from .models import Question

def create_question(question_text, days):
    """
    Create a question with the given question_text, and published
    the given number of days offset to now (negative for question published 
    in the past, positive for question that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days= days)
    return Question.objects.create(question_text= question_text, pub_date=time)

class QuestionModelTest(TestCase):
    def setUp(self):
        self.question  = Question(question_text = 'What is your favourite Python framework?')
        
    def test_was_published_recently_with_future_questions(self):
        """
        was_published_recently returns False 
        for questions whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        #assert
        self.assertIs(self.question.was_published_recently(), False)
    
    def test_was_published_recently_for_past_questions(self):
        """
        the function must return False if the question
        was published before a day
        """
        time = timezone.now() + datetime.timedelta(days=31)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_now(self):
        """
        The function must return True because
        the question is already created
        """
        time = timezone.now()
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)

class QuestionIndexViewTest(TestCase):
    def text_no_question(self):
        """
        If not question exist, an appropiate message is displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available yet!")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    
    def test_future_question(self):
        """
        Question with a pub date in the future aren't displayed
        on the index page.
        """
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available yet!")
        self.assertQuerysetEqual(response.context["latest_question_list"],  [])

    def test_future_question(self):
        """
        Question with a pub date in the future aren't displayed
        on the index page.
        """
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available yet!")
        self.assertQuerysetEqual(response.context["latest_question_list"],  [])
    
    def test_past_questions(self):
        """
        Question wit a pub_date in the past are displayed
        on the index page. 
        """
        question = create_question("Past question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],  [question])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past question
        are display
        """
        past_question = create_question(question_text="past question ", days = -30)
        future_question = create_question(question_text="past question ", days = 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], 
            [past_question]
        )

    def test_two_past_question(self):
        """
        The question index page may display multiple question
        """
        past_question = create_question(question_text="past question ", days = -30)
        past_question2 = create_question(question_text="past question 2", days = -40)
        response  = self.client.get(reverse("polls:index"))

        self.assertQuerysetEqual(
            response.context["latest_question_list"], 
            [past_question, past_question2]
        )
class QuestionDetailViewTest(TestCase):

    def past_question(self):
            """"
            The detail view of a question with a pub_date in the past
            displays the question's text
            """
            past_question = create_question(question_text="past question ", days = -30)
            url = reverse("polls:detail", args=(past_question.id,))
            response = self.client.get(url)
            self.assertContains(response, past_question.question_text)

    def test_future_question(self):
        """"
        The detail view of a question with a pub_date in the future
        returns a 404 error not found
        """
        future_question = create_question(question_text="future question ", days = 30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)