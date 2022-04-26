from django.contrib import admin
from .models import Topic, VoteOpinion, RandomOpinion

# Register your models here.
admin.site.register(Topic)
admin.site.register(VoteOpinion)
admin.site.register(RandomOpinion)