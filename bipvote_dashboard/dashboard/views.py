import os
import random
import string
from django.shortcuts import render
from django import forms
from django.db import transaction
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import  Topic, VoteOpinion, VoiceOpinion

import datetime

# Create your views here.
def index(request):
    latest_topic = Topic.objects.order_by('-pub_date').first()
    if(not latest_topic):
        context = {'pos_opinion': None, 'neg_opinion': None, 'latest_pos_opinion_nr': 0, 'latest_neg_opinion_nr': 0}
        return render(request, 'dashboard/index.html', context)
    topic_id = latest_topic.id
    latest_pos_opinion = VoteOpinion.objects.exclude(voice_opinion__isnull=True).filter(topic=topic_id, vote_choice=True).order_by('-pub_date')[:10]
    latest_neg_opinion = VoteOpinion.objects.exclude(voice_opinion__isnull=True).filter(topic=topic_id, vote_choice=False).order_by('-pub_date')[:10]
    general_opinion = VoiceOpinion.objects.exclude(is_general=False).order_by('-pub_date')[:10]
    latest_pos_opinion_nr = VoteOpinion.objects.filter(topic=topic_id, vote_choice=True).order_by('-pub_date').count()
    latest_neg_opinion_nr = VoteOpinion.objects.filter(topic=topic_id, vote_choice=False).order_by('-pub_date').count()

    context = {'pos_opinion': latest_pos_opinion, 'neg_opinion': latest_neg_opinion, 'latest_pos_opinion_nr': latest_pos_opinion_nr, 'latest_neg_opinion_nr': latest_neg_opinion_nr, 'general_opinion': general_opinion}
    return render(request, 'dashboard/index.html', context)

class VoteForm(forms.Form):
    choice = forms.IntegerField(label='choice')
    key = forms.CharField(label='key', max_length=100)
    vote_or_opinion = forms.CharField(label='vote_or_opinion', max_length=100)
    opinion = forms.FileField(label="opinion", required=False)

def write_to_disk(f, file_name):
    with open("/var/www/ict4d/opinions/" + file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))


@csrf_exempt
def vote(request):
    if request.method == 'POST':
        form = VoteForm(request.POST)
        # print(form.errors)
        if form.is_valid():
            auth_key = form.cleaned_data['key']
            if auth_key == 'bipvote':
                latest_topic = Topic.objects.order_by('-pub_date').first()
                if form.cleaned_data['vote_or_opinion'] == '0':
                    q = VoteOpinion(topic=latest_topic, vote_choice=form.cleaned_data['choice'], pub_date=timezone.now())
                    q.save()
                else:
                    if form.cleaned_data['vote_or_opinion'] == '1':
                        opinion_file_name = "opinion" + "_" + timezone.now().strftime("%Y-%m-%d-%H-%M-%S") + random_char(16) + ".wav"
                        is_general = True
                    else:
                        opinion_file_name = "vote" + "_" + timezone.now().strftime("%Y-%m-%d-%H-%M-%S") + random_char(16) + ".wav"
                        is_general = False
                    opinion = request.FILES['opinion']
                    write_to_disk(opinion, opinion_file_name)

                    vOp = VoiceOpinion(vote_url= "/opinions/" + opinion_file_name, is_general=is_general, pub_date=timezone.now())
                    vOp.save()
                    if form.cleaned_data['vote_or_opinion'] == '2':
                        q = VoteOpinion(voice_opinion=vOp, topic=latest_topic, vote_choice=form.cleaned_data['choice'], pub_date=timezone.now())
                        q.save()

    return render(request, 'dashboard/success.html')

def topic(request):
    return render(request, 'dashboard/topic.html')

class TopicForm(forms.Form):
    topic_str = forms.CharField(label='topic_str', max_length=160)

@csrf_exempt
def process_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = Topic()
            new_topic.topic_str = request.POST['topic_str']
            new_topic.save()
    return HttpResponseRedirect(reverse('index'))
