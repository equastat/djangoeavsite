from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Event, Participant, Question, QuestionResponse

# Create your views here.
class IndexView(generic.ListView):
    model=Event
    template_name = 'healtha/index.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        """Return the events (with published surveys)."""
        return Event.objects.order_by('event_date') 
    

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    survey_sorted_questions, report_data = event.eav_report_data()
    return render(request, 'healtha/event_detail.html', {'event': event, 'survey_sorted_questions': survey_sorted_questions, 'report_data': report_data })


def participant_detail(request, event_id, participant_id):
    event = get_object_or_404(Event, pk=event_id)
    participant = get_object_or_404(Participant, pk=participant_id)
    participant_response = participant.get_response_dict()
    
    print(participant_response)
    return render(request, 'healtha/participant_detail.html', {'event': event, 'participant': participant, 'participant_response': participant_response })

    
def participant(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'healtha/participant.html', {'event': event})    


def participant_add(request, event_id):
    participant = Participant.objects.create(name=request.POST['participant_name'], event_id=event_id)
    return HttpResponseRedirect(reverse('healtha:participant_detail', args=(event_id, participant.id,)))

    
def participant_question(request, event_id, participant_id, question_id):
    event = get_object_or_404(Event, pk=event_id)
    participant = get_object_or_404(Participant, pk=participant_id, event_id=event_id)
    selected_question = get_object_or_404(Question, pk=question_id)
    sorted_questions = event.survey.get_sorted_questions()
    question_count = sorted_questions.count()
    question_ordinal = 0
    # 1-based index of selected question in event survey
    selected_question_ordinal = 0
    
    for question in sorted_questions:        
        question_ordinal += 1
        if question.id == selected_question.id:
            selected_question_ordinal = question_ordinal
            break
    
    if selected_question_ordinal == 0:
        # Asked for a question not in this event's survey
        raise Exception('Question not in selected event survey')
    
    if question_ordinal < question_count:
        next_question = sorted_questions[question_ordinal]
    else:
        next_question =  None

    if question_ordinal > 1:
        previous_question = sorted_questions[question_ordinal-2]
    else:
        previous_question = None
    
    question_response = QuestionResponse.objects.filter(participant_id=participant.id,question_id=selected_question.id).first()
    
    return render(request, 'healtha/participant_question.html', {'event': event, 'participant': participant, 'question': selected_question, 'question_count': question_count, 'question_ordinal': question_ordinal, 'sorted_questions': sorted_questions, 'next_question': next_question, 'previous_question': previous_question, 'question_response': question_response })

    
def participant_response(request, event_id, participant_id, question_id):
    participant = get_object_or_404(Participant, pk=participant_id, event_id=event_id)
    question_response, created = QuestionResponse.objects.get_or_create(participant_id=participant_id,question_id=question_id)
    question_response.value = request.POST['question_response_text']
    question_response.save()
    
    if 'next_question_id' in request.POST and request.POST['next_question_id']:
        return HttpResponseRedirect(reverse('healtha:participant_question', args=(event_id, participant_id,request.POST['next_question_id'],)))
    else:
        return HttpResponseRedirect(reverse('healtha:participant_detail', args=(event_id, participant_id,)))

    
