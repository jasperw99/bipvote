from django.contrib import admin
from .models import Topic, VoteOpinion, VoiceOpinion

# Register your models here.
admin.site.register(Topic)
admin.site.register(VoteOpinion)
admin.site.register(VoiceOpinion)