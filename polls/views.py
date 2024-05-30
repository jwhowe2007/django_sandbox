from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Question

import datetime

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    context = {
        "questions": latest_question_list
    }

    return render(request, "polls/index.html", context)

def question_detail(request, question_id):
    # pk=x indicates that x is a primary key of the object being referred to.
    question = get_object_or_404(Question, pk=question_id)

    return render(request, "polls/questions/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Refresh the question voting form.
        return render(
            request,
            "polls/questions/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice."
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=[question.id]))
