from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Models
from .models import Question, Choice
def index(request):
    latest_question_list = Question.objects.all 
    return render(request, 'polls/index.html', {
        'latest_question_list': latest_question_list
    })
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {
        'question': question
    })
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {
        'question': question
    })
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_question = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question, 
            'error_message': 'Please choose a correct option.'
        })
    else:
        selected_question.votes =+ 1
        selected_question.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    