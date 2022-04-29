from django.db import models
from django.utils import timezone

# Create your models here.
class Topic(models.Model):
    topic_str = models.CharField(max_length=200, blank=True)
    topic_sound = models.CharField(max_length=200, blank=True)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    def __str__(self):
        if self.topic_str:
            return self.topic_str
        return self.id

class VoteOpinion(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    vote_choice = models.BooleanField()
    vote_opinion = models.CharField(max_length=200, null=True)
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return f"vote_opinion_{self.topic}_{self.vote_choice}_{self.pub_date}"

class RandomOpinion(models.Model):
    vote_opinion = models.CharField(max_length=200)
