from django.contrib import admin

from .models import Question, Event, Survey, Participant

# Register your models here.
admin.site.register(Question)
admin.site.register(Event)
admin.site.register(Survey)

admin.site.register(Participant)
