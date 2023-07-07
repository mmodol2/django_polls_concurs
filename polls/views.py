from django.http import Http404
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.db.models import Sum

from django.http import JsonResponse

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class ConcursView(generic.ListView):
    model = Question
    template_name = "polls/concurs.html"
    context_object_name = "question_list"

    def get_queryset(self):
        """ Llista amb les pregunta ordenades  amb el total de vots major ."""
        return Question.objects.annotate(total_votes=Sum('choice__votes')).order_by('-total_votes')    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ll_preguntes_vots'] = [(question, question.total_votes) for question in context['object_list']]
        return context

# def index(request):
#     # latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     # output = ", ".join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("polls/index.html")
#     context = { "latest_question_list": latest_question_list }
#     # return HttpResponse(template.render(context, request))
#     return render(request, "polls/index.html", context)

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})
    
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, "polls/detail.html", {"question": question})

#     # return HttpResponse("You're looking at question %s." % question_id)

# def results(request, question_id):
#     # response = "You're looking at the results of question %s."
#     # return HttpResponse(response % question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})


# captura el vot sense classes
def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {   "question": question,
                "error_message": "You didn't select a choice.", },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def obtener_datos_grafica(request, question_id):
    question = Question.objects.get(id=question_id)
    choices = question.choice_set.all()

    labels = []
    values = []
    for choice in choices:
        labels.append(choice.choice_text)
        values.append(choice.votes)

    data = {
        'labels': labels,
        'values': values,
    }

    return JsonResponse(data)
