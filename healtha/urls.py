"""djangoeavsite\healtha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views
app_name = 'healtha'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^(?P<event_id>[0-9]+)/$', views.event_detail, name="event_detail"),
    url(r'^(?P<event_id>[0-9]+)/participant/(?P<participant_id>[0-9]+)$', views.participant_detail, name="participant_detail"),
    url(r'^(?P<event_id>[0-9]+)/participant$', views.participant, name="participant"),
    url(r'^(?P<event_id>[0-9]+)/participant/(?P<participant_id>[0-9]+)/question/(?P<question_id>[0-9]+)$', views.participant_question, name="participant_question"),
    url(r'^(?P<event_id>[0-9]+)/participant/(?P<participant_id>[0-9]+)/question/(?P<question_id>[0-9]+)/response$', views.participant_response, name="participant_response"),
    url(r'^(?P<event_id>[0-9]+)/participant/add$', views.participant_add, name="participant_add"),
]
