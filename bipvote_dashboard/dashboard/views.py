from django.shortcuts import render
from django import forms
from django.db import transaction
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import  Topic, VoteOpinion

import datetime

# Create your views here.
def index(request):
    latest_topic = Topic.objects.order_by('-pub_date').first()
    if(not latest_topic):
        context = {'pos_opinion': None, 'neg_opinion': None, 'latest_pos_opinion_nr': 0, 'latest_neg_opinion_nr': 0}
        return render(request, 'dashboard/index.html', context)
    topic_id = latest_topic.id
    latest_pos_opinion = VoteOpinion.objects.exclude(vote_opinion__isnull=True).filter(topic=topic_id, vote_choice=True).order_by('-pub_date')[:10]
    latest_neg_opinion = VoteOpinion.objects.exclude(vote_opinion__isnull=True).filter(topic=topic_id, vote_choice=False).order_by('-pub_date')[:10]
    latest_pos_opinion_nr = VoteOpinion.objects.filter(topic=topic_id, vote_choice=True).order_by('-pub_date').count()
    latest_neg_opinion_nr = VoteOpinion.objects.filter(topic=topic_id, vote_choice=False).order_by('-pub_date').count()

    context = {'pos_opinion': latest_pos_opinion, 'neg_opinion': latest_neg_opinion, 'latest_pos_opinion_nr': latest_pos_opinion_nr, 'latest_neg_opinion_nr': latest_neg_opinion_nr}
    return render(request, 'dashboard/index.html', context)

class VoteForm(forms.Form):
    choice = forms.IntegerField(label='choice')
    key = forms.CharField(label='key', max_length=100)

@csrf_exempt
def vote(request):
    if request.method == 'POST':
        form = VoteForm(request.POST)

        if form.is_valid():
            auth_key = form.cleaned_data['key']
            if auth_key == 'bipvote':
                choice = form.cleaned_data['choice']
                latest_topic = Topic.objects.order_by('-pub_date').first()
                q = VoteOpinion(topic=latest_topic, vote_choice=form.cleaned_data['choice'], pub_date=timezone.now())
                q.save()

    return render(request, 'dashboard/success.html')

def topic(request):
    return render(request, 'dashboard/topic.html')

def process_topic(request):
    new_topic = Topic()
    new_topic.topic_str = request.POST['topic_str']
    new_topic.save()
    return HttpResponseRedirect(reverse('index'))
