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

class VoiceOpinion(models.Model):
    vote_url = models.CharField(max_length=200)
    is_general = models.BooleanField()
    pub_date = models.DateTimeField('date published', default=timezone.now)


class VoteOpinion(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    vote_choice = models.BooleanField()
    voice_opinion = models.ForeignKey(VoiceOpinion, on_delete=models.CASCADE, blank=True, null=True)
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return f"vote_opinion_{self.topic}_{self.vote_choice}_{self.pub_date}"


