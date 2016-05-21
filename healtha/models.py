from django.db import models

# Create your models here.
QUESTION_TYPES_TUPLE = (
    ('StringValue', 'String'),
    ('IntegerValue', 'Integer'),
)


class Question(models.Model):
    question_text = models.CharField(max_length=250)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES_TUPLE)

    def __str__(self):
        return self.question_text


class Survey(models.Model):
    survey_name = models.CharField(max_length=250)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.survey_name
    
    def get_sorted_questions(self):
        return self.questions.all().order_by('id')
        

class Event(models.Model):
    survey = models.ForeignKey('Survey', null=True)
    event_date = models.DateTimeField(null=True)

    def __str__(self):
        return "Event %s %s:%s" % (self.id, self.event_date, self.survey)
        
    def eav_report_data(self):
        report_data = []
        participants = self.participant_set.order_by('name').prefetch_related('questionresponse_set')
        questions = self.survey.get_sorted_questions()
        for participant in participants:
            participant_data = [ participant.id, participant.name ]
            participant_responses = participant.get_response_dict()
            for question in questions:
                if question.id in participant_responses:
                    participant_data.append(participant_responses[question.id])
                else:
                    participant_data.append(None)
            report_data.append(participant_data)
        return questions, report_data
        

class Participant(models.Model):
    name = models.CharField(max_length=250, null=True)
    event = models.ForeignKey(Event, null=True)
    date_completed = models.DateTimeField(null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s at %s:%s" % (self.name, self.event, self.date_completed)
    
    def get_response_dict(self):
        response_dict = dict()
        for question_response in self.questionresponse_set.all():
            response_dict[question_response.question_id] = question_response.value
        return response_dict

        
class QuestionResponse(models.Model):
    participant = models.ForeignKey(Participant)
    question = models.ForeignKey(Question)
    value = models.TextField()

    def __str__(self):
        return "%s: %s" % (self.question, self.value)

    class Meta:
        unique_together = ('participant', 'question')

    def get_input_obj(self):
        return self.question.get_input_obj(self.participant)


