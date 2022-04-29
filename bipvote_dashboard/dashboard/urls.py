from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vote/', views.vote, name='vote'),
    path('topic/', views.topic, name='topic'),
    path('process_topic/', views.process_topic, name='process_topic'),
]