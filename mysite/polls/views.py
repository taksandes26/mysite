from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, Http404
from .models import Question, Choice
from django.template import loader
from django.urls import reverse


def index(request):
    latest_question_list = Question.objects.order_by("-publish_date")
    template = loader.get_template("polls/index.html")
    context = {"latest_question_list": latest_question_list}
    return HttpResponse(template.render(context, request))


def detail_page(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)
    except Question.DoesNotExist:
        raise Http404("question does not exist.")
    return render(request, 'polls/detail.html', {'question': question})


def results_page(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {'question': question, 'error_message': "you didn't "
                                                                                      "select a choice "})

    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('results_page', args=(question.id,)))
